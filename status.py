from i3pystatus import Status
from datetime import datetime
from pathlib import Path

logtime = Path(f"/home/user/status_bar/logs/{datetime.now().strftime('%Y%m%d') }.log")
status = Status(logfile=logtime)

COLOR_DISK_BG       = '#FFFFFF'
COLOR_WIFI_BG       = '#415A77'
COLOR_BATTERY_BG    = '#5C7D53'
COLOR_CPU_BG        = '#D62828'
COLOR_SOUND_BG      = '#FFECD1'
COLOR_IP_EXT_BG     = '#D18B14'


ALERT_RED           = '#D62828'
BLUE_ON_WHITE       = '#15616D'
AMBER_ON_WHITE      = '#FF7D00'


# Displays clock like this:
# Tue 30 Jul 11:59:46 PM 
status.register("clock",
    format="%a %d/%m/%y  %X",
    hints = {
        'min_width': 150,
        'align'    : 'center'
    })

status.register("cpu_usage",
                format="{usage:>4}%",
                hints = {
                    'background': COLOR_CPU_BG,
                    'min_width' : 40,
                    'align'     : "center"
                        }
                )
status.register("temp",
                format="  CPU  {temp:.0f}°C",
                hints = {"separator": False,
                         "separator_block_width":0,
                         'background': COLOR_CPU_BG,
                         'align'     : "center",})

# The battery monitor has many formatting options, see README for details
status.register("battery",
    format="{status} {consumption:.2f}W {percentage:.2f}% {remaining:%E%hh:%Mm}",
    full_color = "#FFFFFF",
    interval = 1,
    alert=True,
    alert_percentage=10,
    not_present_text = "no battery installed",
    not_present_color = "#D00000",
    status={
        "DIS": "↓",
        "CHR": "↑",
        "FULL": "=",
    }, hints = {
    'background' : COLOR_BATTERY_BG,
    'align'     : "center",
    'min_width': 190,
    "separator": False,
    })

# Note: requires both netifaces and basiciw (for essid and quality)
status.register("network",
    interface="wlp3s0",
    format_up="{quality:3.0f}% {essid} {v4}",
    color_up="#FFFFFF",
    color_down="#F48C06",
    hints = {
    'background' : COLOR_WIFI_BG,
    'align'     : "center",
    'min_width': 230,
    "separator": False,
    })

status.register("external_ip",
                format="{country_code} {ip}",
                hints = {
                    'background': COLOR_IP_EXT_BG
                })


status.register("disk",
    path="/",
    format="{used}/{total}G [{avail}]G",
    display_limit = 10,
    color = "#000000",
    critical_color = ALERT_RED,
    hints = {
    'background': COLOR_DISK_BG,
    'align'     : "center",
    'min_width': 180,
    "separator": False,
    })

status.register("shell",
                command = "source /home/user/status_bar/.venv/bin/activate; /home/user/status_bar/.venv/bin/python /home/user/status_bar/modules/asylum/mediusWLAN.py",
                interval = 864,
                hints = {
                    'background'            : COLOR_WIFI_BG,
                    'separator'             : False,
                    'separator_block_width' : 10,
                    'min_width'             : 550,
                    'align'                 : 'center',
                    "separator": False,
                    }
                )

status.register("pulseaudio",
    format="♪{volume}",
            color_muted = AMBER_ON_WHITE,
            color_unmuted = BLUE_ON_WHITE,
            hints = {
                'background' : COLOR_SOUND_BG,
                'align'     : "center",
                'min_width': 70,
                "separator": False,
                },
            )

status.register("bluetooth",
                format = "{name}",
                color = BLUE_ON_WHITE,
                connected_color=BLUE_ON_WHITE,
                on_leftclick = "blueman-manager",
                hints = {
                    'background' : COLOR_SOUND_BG,
                    'align'     : "center",
                    'min_width': 70,
                    "separator": False,
                },
)



# Shows mpd status
# Format:
# Cloud connected ▶ Reroute to Remain
status.register("mpd",
    format="{title}{status}{album}",
    status={
        "pause": "▷",
        "play" : "▶",
        "stop" : "◾",
    },)

status.run()