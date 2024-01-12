```yaml
themes:
    name: light
    base: theme-light
data_source: foobar # this is the dictionary to search through
```

```html
<input id="search" class="w3-input w3-round search-bar ${{ themes.name }} ${{ themes.base }}" type="text" name="search" placeholder="Search" style="margin-right:4px;margin-top:8px;margin-bottom:8px;" oninput="doSearch()">
</div>
```

```css
.search-bar {
    width:80%;
    margin-left:5%;
}
```

```js
var hidden = []

function render() {
    let prefix = $("#search").val();
    prefix = prefix.toLowerCase();

    if (prefix == "") {
        hidden = []
    } else {
        for (let [key, task] of Object.entries(${{ data_source }})) {
            if (key.toLowerCase().indexOf(prefix) == -1) {
                hidden.push(key)
            }
        }
    }
    
    for (let [key, task] of Object.entries(${{ data_source }})) {
        $(`#${key}`).css("filter", `brightness(100%)`)

        if (hidden.includes(key)) {
            $(`#${key}`).css("filter", `brightness(50%)`)
        }
    }
}
```
