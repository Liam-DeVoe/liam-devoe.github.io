serve:
    # Exit early on errors. Apparently --listen doesn't do this even if we
    # add --fatal=errors to it.
    python3 -m pelican content --fatal=errors
    open http://127.0.0.1:8000
    python3 -m pelican --listen
