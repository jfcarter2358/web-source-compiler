```yaml
title: Foobar
links: 
    title: /ui/foobar
    logout: /auth/logout
title_lower: foobar
color: '#A3BE8C'
themes: 
    name: light
    base: theme-light
    border: theme-border-light
    text: theme-text
    hover: theme-hover-text-dark
```

```js
function toggleMenu() {
    var x = document.getElementById("user-menu");
    if (x.className.indexOf("w3-show") == -1) { 
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}
```

```html
<div class="w3-bar ${{ themes.name }} header-color w3-card-4 w3-border ${{ themes.border }} w3-padding">
    <div class="w3-large ${{ themes.name }} w3-container w3-cell w3-cell-middle w3-left-align default-cursor breadcrumb" style="display:inline-block;margin-top:10px;">
        <i class="fa-solid fa-bars w3-large" onclick="toggleSidebar()"></i>
    </div>
    <div class="w3-large ${{ themes.name }} w3-container w3-cell w3-cell-middle w3-right-align breadcrumb" style="display:inline-block;margin-top:10px;">
        <a href="${{ links.title }}" class="${{ themes.name }} ${{ themes.text }}">${{ title }}</a>
    </div>
    <div class="w3-dropdown-click ${{ themes.name }}} w3-container" style="float:right;margin-right:8px;margin-top:2px;">
        <i class="fa-solid fa-circle-user pointer-cursor w3-xxxlarge ${{ themes.name }}" onclick="toggleMenu()"></i>
        <div class="w3-dropdown-content w3-bar-block w3-round" style="position:absolute;right:40px;top:56px;background-color: transparent;" id="user-menu">
            <div class="${{ themes.name }} w3-border">
                <a href="${{ links.logout }}" class="w3-bar-item w3-button ${{ themes.name }} ${{ themes.base }} header-hover" style="position:relative;z-index:100">Logout</a>
            </div>
        </div>
    </div>
    <div class="w3-large ${{ themes.name }} w3-container w3-cell breadcrumb" style="float:right;margin-top:10px;">
        <span class="${{ themes.name }} ${{ themes.text }}">{{ .family_name }}, {{ .given_name }}</span>
    </div>
</div>
```

```css
.header-color,.header-hover:hover{color:#fff!important;background-color:${{ color }}!important}
```
