```yaml
color: '#A3BE8C'
themes:
    name: light
    base: theme-light
    border: theme-border-light
    table: theme-table-striped
```

```py
require jfcarter2358.sidebar
import jfcarter2358.modal
```

```html
<jfcarter2358.modal>
title: Status Modal
contents: |
    <table class="w3-table light w3-border ${{ themes.border }} ${{ themes.table }}" id="status-table">
    </table>
id: status-modal
color: "${{ color }}"
themes:
    name: ${{ themes.name }}
    base: ${{ themes.base }}
    border: ${{ themes.border }}
    table: ${{ themes.table }}
</jfcarter2358.modal>
```

```js
allHealthClasses = ""
healthIntervalMilliSeconds = "5000"
var healthIcons = {
	'healthy': 'fa-circle-check',
	'degraded': 'fa-circle-exclamation',
	'unhealthy': 'fa-circle-xmark',
	'unknown': 'fa-circle-question'
}

var healthColors = {
	'healthy': 'scaffold-text-green',
	'degraded': 'scaffold-text-yellow',
	'unhealthy': 'scaffold-text-red',
	'unknown': 'scaffold-text-charcoal'
}

var healthText = {
	'healthy': 'Up',
	'degraded': 'Degraded',
	'unhealthy': 'Down',
	'unknown': 'Unknown'
}

var icons = {
	'healthy': 'fa-circle-check',
	'warn': 'fa-circle-exclamation',
	'error': 'fa-circle-xmark',
	'deploying': 'fa-spinner fa-pulse',
	'unknown': 'fa-circle-question',
	'not-deployed': 'fa-circle'
}

var colors = {
	'healthy': 'green',
	'warn': 'yellow',
	'error': 'red',
	'deploying': 'grey',
	'unknown': 'orange',
	'not-deployed': 'grey'
}


function populateVariables() {
    for (var key in healthIcons) {
        allHealthClasses += healthIcons[key] + " "
    }
    for (var key in healthColors) {
        allHealthClasses += healthColors[key] + " "
    }
}

function countJSON(json) {
    var count = 0;
    for (var key in json) {
        if (json.hasOwnProperty(key)) {
            count++;
        }
    }
    return count
}

function updateStatuses() {
    $.ajax({
        url: "/health/status",
        type: "GET",
        success: function (result) {
            tableInnerHTML = '<tr>' +
                '<th class="table-title w3-medium status-text">' +
                '</th>' +
                '<th class="table-title w3-medium status-text">' +
                    '<span class="table-title-text">Service</span>' +
                '</th>' +
                '<th class="table-title w3-medium status-text">' +
                    '<span class="table-title-text">Status</span>' +
                '</th>' +
                '<th class="table-title w3-medium status-text">' +
                    '<span class="table-title-text">Version</span>' +
                '</th>' +
            '</tr>'

            let is_healthy = true
            let down_count = 0

            for (let i = 0; i < result.nodes.length; i++) {
                serviceStatusColor = healthColors[result.nodes[i].status]
                serviceStatusText = healthText[result.nodes[i].status]
                serviceStatusIcon = healthIcons[result.nodes[i].status]
                serviceStatusVersion = result.nodes[i].version
                if (result.nodes[i].status != 'healthy') {
                    is_healthy = false
                    down_count += 1
                }
                tableInnerHTML += '<tr>' +
                    '<td class="status-table-icon ' + serviceStatusColor + ' ' + serviceStatusIcon + '">' + '</td>' +
                    '<td>' + result.nodes[i].name + '</td>' +
                    '<td class="status-table-status">' + serviceStatusText + '</td>' +
                    '<td>' + serviceStatusVersion + '</td>' +
                '</tr>'
            }
            $("#status-table").html(tableInnerHTML)
            $("#status-icon").removeClass(allHealthClasses)
            if (down_count == result.nodes.length) {
                $("#status-icon").addClass(healthIcons["unhealthy"] + " " + healthColors["unhealthy"])
            } else if (is_healthy) {
                $("#status-icon").addClass(healthIcons["healthy"] + " " + healthColors["healthy"])
            } else {
                $("#status-icon").addClass(healthIcons["degraded"] + " " + healthColors["healthy"])
            }
        },
        error: function (result) {
            tableElements = $('.status-table-icon')
            for (let i = 0; i < tableElements.length; i++) {
                $(tableElements[i]).removeClass(allHealthClasses)
                $(tableElements[i]).addClass(healthColors['unknown'])
                $(tableElements[i]).addClass(healthIcons['unknown'])
            }

            tableElements = $('.status-table-status')
            for (let i = 0; i < tableElements.length; i++) {
                $(tableElements[i]).text(healthText['unknown'])
            }

            $("#status-icon").removeClass(allHealthClasses)
            $("#status-icon").addClass(healthIcons["unknown"] + " " + healthColors["unknown"])
        }
    });
}

function showStatus() {
    toggleSidebar()
    openModal('status-modal')
}

$(document).ready(
    function() {
        populateVariables()
        updateStatuses()
        setInterval(updateStatuses, healthIntervalMilliSeconds);
    }
)
```

```css
.status-text,.status-hover-text:hover{color:${{ color }}!important}
```
