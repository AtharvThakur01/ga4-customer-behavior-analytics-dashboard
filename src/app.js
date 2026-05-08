const rows = [
  { channel: "Organic Search", segment: "New users", users: 18420, sessions: 23680, engaged: 15140, views: 52100, addToCart: 2060, checkout: 1220, purchases: 645, revenue: 84250 },
  { channel: "Paid Search", segment: "Returning users", users: 10180, sessions: 14840, engaged: 10760, views: 34590, addToCart: 1810, checkout: 1088, purchases: 590, revenue: 76670 },
  { channel: "Email", segment: "Loyal customers", users: 7260, sessions: 10340, engaged: 8410, views: 26320, addToCart: 1630, checkout: 1124, purchases: 721, revenue: 94230 },
  { channel: "Paid Social", segment: "New users", users: 12740, sessions: 15420, engaged: 8490, views: 29410, addToCart: 1280, checkout: 604, purchases: 276, revenue: 33880 },
  { channel: "Referral", segment: "High intent", users: 4860, sessions: 6120, engaged: 4390, views: 14260, addToCart: 740, checkout: 466, purchases: 254, revenue: 32120 },
  { channel: "Direct", segment: "Returning users", users: 9340, sessions: 12880, engaged: 9230, views: 30140, addToCart: 1185, checkout: 774, purchases: 438, revenue: 55190 }
];

const events = [
  { name: "page_view", countKey: "views", owner: "Web analytics" },
  { name: "user_engagement", countKey: "engaged", owner: "Product" },
  { name: "add_to_cart", countKey: "addToCart", owner: "Merchandising" },
  { name: "begin_checkout", countKey: "checkout", owner: "Lifecycle" },
  { name: "purchase", countKey: "purchases", owner: "Revenue" }
];

const channelFilter = document.querySelector("#channelFilter");
const segmentFilter = document.querySelector("#segmentFilter");

const formatNumber = new Intl.NumberFormat("en-US");
const formatCurrency = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });
const formatPercent = (value) => `${(value * 100).toFixed(1)}%`;

function uniqueValues(key) {
  return [...new Set(rows.map((row) => row[key]))].sort();
}

function hydrateFilters() {
  uniqueValues("channel").forEach((value) => channelFilter.append(new Option(value, value)));
  uniqueValues("segment").forEach((value) => segmentFilter.append(new Option(value, value)));
}

function currentRows() {
  return rows.filter((row) => {
    const channelMatch = channelFilter.value === "all" || row.channel === channelFilter.value;
    const segmentMatch = segmentFilter.value === "all" || row.segment === segmentFilter.value;
    return channelMatch && segmentMatch;
  });
}

function total(data, key) {
  return data.reduce((sum, row) => sum + row[key], 0);
}

function render() {
  const data = currentRows();
  const users = total(data, "users");
  const engaged = total(data, "engaged");
  const purchases = total(data, "purchases");
  const revenue = total(data, "revenue");
  const views = total(data, "views");
  const checkout = total(data, "checkout");

  const kpis = [
    { label: "Total users", value: formatNumber.format(users), note: `${formatPercent(engaged / users)} engaged sessions` },
    { label: "Purchases", value: formatNumber.format(purchases), note: `${formatPercent(purchases / users)} user conversion rate` },
    { label: "Revenue", value: formatCurrency.format(revenue), note: `${formatCurrency.format(revenue / Math.max(purchases, 1))} average order value` },
    { label: "Checkout completion", value: formatPercent(purchases / checkout), note: `${formatNumber.format(checkout)} begin_checkout events` }
  ];

  document.querySelector("#overview").innerHTML = kpis
    .map((kpi) => `<article class="metric"><span>${kpi.label}</span><strong>${kpi.value}</strong><small>${kpi.note}</small></article>`)
    .join("");

  document.querySelector("#conversionRate").textContent = `${formatPercent(purchases / users)} conversion rate`;

  const funnel = [
    ["Users", users],
    ["Page views", views],
    ["Add to cart", total(data, "addToCart")],
    ["Checkout", checkout],
    ["Purchase", purchases]
  ];
  const maxFunnel = Math.max(...funnel.map((item) => item[1]));
  document.querySelector("#funnel").innerHTML = funnel
    .map(([label, value]) => `
      <div class="funnel-row">
        <strong>${label}</strong>
        <div class="bar-track"><div class="bar" style="width:${(value / maxFunnel) * 100}%"></div></div>
        <span>${formatNumber.format(value)}</span>
      </div>
    `)
    .join("");

  document.querySelector("#segments").innerHTML = Object.entries(groupBy(data, "segment"))
    .map(([segment, segmentRows]) => {
      const segmentUsers = total(segmentRows, "users");
      const segmentRevenue = total(segmentRows, "revenue");
      return `<div class="segment"><strong>${segment}<span>${formatCurrency.format(segmentRevenue)}</span></strong><small>${formatNumber.format(segmentUsers)} users</small></div>`;
    })
    .join("");

  const eventMax = Math.max(...events.map((event) => total(data, event.countKey)));
  document.querySelector("#eventsList").innerHTML = events
    .map((event) => {
      const count = total(data, event.countKey);
      return `<div class="event"><strong>${event.name}<span>${formatNumber.format(count)}</span></strong><small>Owner: ${event.owner}</small><div class="event-meter"><span style="width:${(count / eventMax) * 100}%"></span></div></div>`;
    })
    .join("");

  document.querySelector("#channelTable").innerHTML = Object.entries(groupBy(data, "channel"))
    .map(([channel, channelRows]) => {
      const channelUsers = total(channelRows, "users");
      const channelPurchases = total(channelRows, "purchases");
      return `<tr><td>${channel}</td><td>${formatNumber.format(channelUsers)}</td><td>${formatNumber.format(channelPurchases)}</td><td>${formatCurrency.format(total(channelRows, "revenue"))}</td><td>${formatPercent(channelPurchases / channelUsers)}</td></tr>`;
    })
    .join("");

  const bestChannel = [...data].sort((a, b) => b.purchases / b.users - a.purchases / a.users)[0];
  const dropOff = checkout ? 1 - purchases / checkout : 0;
  const insightCards = [
    { title: "Scale efficient acquisition", detail: `${bestChannel?.channel || "Email"} has the strongest conversion rate. Use this channel as the benchmark for campaign QA and landing-page messaging.` },
    { title: "Reduce checkout drop-off", detail: `${formatPercent(dropOff)} of checkout starters do not purchase. Prioritize payment friction, promo-code errors, and shipping-cost visibility.` },
    { title: "Improve event reliability", detail: "Validate add_to_cart, begin_checkout, and purchase parameters weekly before Looker Studio stakeholder reporting refreshes." },
    { title: "Segment next experiments", detail: "Separate first-time and returning users in GA4 explorations to avoid blended conversion reads and unclear ownership." }
  ];
  document.querySelector("#insightGrid").innerHTML = insightCards
    .map((card) => `<article class="insight-card"><strong>${card.title}</strong><small>${card.detail}</small></article>`)
    .join("");
}

function groupBy(data, key) {
  return data.reduce((groups, row) => {
    groups[row[key]] = groups[row[key]] || [];
    groups[row[key]].push(row);
    return groups;
  }, {});
}

hydrateFilters();
render();
channelFilter.addEventListener("change", render);
segmentFilter.addEventListener("change", render);
