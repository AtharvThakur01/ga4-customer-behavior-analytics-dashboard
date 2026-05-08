# GA4 Measurement Plan

## Business Questions

- Which acquisition channels drive engaged users and purchase conversion?
- Where do customers drop between browsing, cart, checkout, and purchase?
- Which audience segments should stakeholders prioritize for experiments?
- Are GA4 events complete enough for weekly Looker Studio reporting?

## Event Tracking Design

| Event | Trigger | Required Parameters | Success Criteria |
| --- | --- | --- | --- |
| `page_view` | Page route loads | `page_location`, `page_title`, `content_group` | Every tracked page has one clean event per view |
| `view_item` | Product detail viewed | `item_id`, `item_name`, `item_category`, `price` | Product engagement can be tied to catalog data |
| `add_to_cart` | User adds product to cart | `item_id`, `quantity`, `value`, `currency` | Cart intent can be segmented by channel |
| `begin_checkout` | Checkout begins | `cart_id`, `value`, `currency`, `coupon` | Checkout drop-off is measurable |
| `purchase` | Payment confirmation | `transaction_id`, `value`, `currency`, `items` | Conversion and revenue reporting are reliable |

## Conversions

Primary conversion: `purchase`

Supporting conversions:

- `generate_lead`
- `sign_up`
- `begin_checkout`

## QA Checklist

- Confirm events are visible in GA4 DebugView before release.
- Validate ecommerce parameters with Tag Assistant.
- Compare backend orders with GA4 purchase counts within an accepted variance threshold.
- Check consent mode behavior for analytics storage.
- Review Looker Studio filters after schema or naming changes.
