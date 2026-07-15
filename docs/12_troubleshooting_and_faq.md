# 12. Troubleshooting & FAQ

Are you having trouble getting TraceNest to work? Here are the most common problems and how to fix them!

## The UI is blank / I don't see any logs!
**Problem:** You mounted the UI in FastAPI, opened the dashboard, but the table is completely empty.
**Solution:** 
1. **Have you written any logs yet?** TraceNest only shows logs that have been saved to the `app.log` file. If your Python code hasn't executed `logger.info()` yet, the file is empty! Run a function in your app that triggers a log, and then refresh the UI.
2. **Check your working directory!** The dashboard looks for the `logs/app.log` file relative to where you started the server. If you start your FastAPI server from a different folder than where your logs are saving, the UI won't be able to find the file.

## I'm getting a "Permission Denied" error!
**Problem:** Your app crashes with `PermissionError: [Errno 13] Permission denied: 'logs/app.log'`.
**Solution:** This means the user account running your Python script does not have permission to create folders or write files in that directory. 
* *Fix:* Run your app in a folder where you have write access, or change the `log_dir` in `TraceNestConfig` to a folder like `/tmp/` or your home directory.

## Can I change the colors of the dashboard?
**Solution:** Yes! Click the palette icon in the top right corner of the dashboard to choose between 6 different themes, including Light, Dark, Dark Blue, Emerald, Ruby, and Midnight.

## Does TraceNest slow down my app?
**Solution:** No! TraceNest uses an asynchronous background thread to write logs to your hard drive. This means your main app never stops to wait for the hard drive to finish saving.

---
**Next Step:** Want to help make TraceNest better? Read [13. Contributing](13_contributing.md).
