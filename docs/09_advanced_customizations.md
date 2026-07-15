# 09. Advanced Customizations

TraceNest was built to be completely flexible. If you don't like how it formats your logs by default, you can easily write your own Formatter!

## Writing a Custom Formatter

By default, TraceNest uses a `JsonFormatter` which turns your logs into JSON strings so the UI can read them. But let's say you want to write logs to a plain text file for a legacy system.

You can create your own Formatter by extending `logging.Formatter`:

```python
import logging
from tracenest.logger import get_logger
from tracenest.core.config import TraceNestConfig

# 1. Create a custom formatter class
class MyPlaintextFormatter(logging.Formatter):
    def format(self, record):
        # record is an object containing all the log details
        return f"[{record.levelname}] {record.msg} (Custom!)"

# 2. Tell TraceNest to use your formatter!
# Wait, TraceNest doesn't support custom formatters in the config directly yet.
# But you can attach it to the underlying logger!
```

*Note: The TraceNest Dashboard UI specifically requires logs to be formatted as JSON using the built-in `TraceNestJsonFormatter`. If you change the formatter to plain text, the Web UI will not be able to display your logs!*

## Adding Extra Data (Context) to Logs

One of the best features of TraceNest is the ability to attach extra variables to your logs. 

Instead of typing:
`logger.info(f"User {user_id} bought item {item_id}")`

You can type:
`logger.info("User completed purchase", user_id=user_id, item_id=item_id)`

This is *much* better because the `user_id` and `item_id` will be saved as separate variables in the JSON file. When you click on the log in the Web Dashboard, those variables will appear beautifully formatted in the Details Panel!

---
**Next Step:** Are you ready to put this on the internet? Read [10. Deployment & Production](10_deployment_and_production.md).
