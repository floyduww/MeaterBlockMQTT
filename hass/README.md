# This is the Home Assistant side.

The lovelace interface needs card-mod.js for the block status badge.  
https://github.com/thomasloven/lovelace-card-mod

Also needs the MQTT Integration

lovelace_dashboard.yaml was pulled from the lovelace raw editor

# starting the script
Add to your configuration.yaml
```
shell_command:
    meater_block: 'python3 /pathtoscript/meater_reader_buf.py' 
```

# Start the script automatically via Node-Red when Meater Block connects to wifi

Add the node_red.json to a flow.
