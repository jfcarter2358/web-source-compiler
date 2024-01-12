```yaml
contents: <h2>Foobar</h2>
id: foo-modal
title: Foo Modal
color: '#A3BE8C'
themes:
    name: light
    base: theme-light
    border: theme-border-light
    table: theme-table-striped
```

```js
function closeModal(modalID) {
    document.getElementById(modalID).style.display='none'
}

function openModal(modalID) {
    document.getElementById(modalID).style.display='block'
}
```

```html
<div id="${{ id }}" class="w3-modal" style="z-index:999;">
    <div class="w3-modal-content w3-animate-top w3-card-4 w3-round light theme-light w3-border ${{ themes.border }} w3-round">
        <header class="w3-container ${{ id }}-modal-color">
            <span onclick="closeModal('${{ id }}')" class="w3-button w3-display-topright">&times;</span>
            <h4>System Status</h4>
        </header>
        <div class="w3-container">
            <br>
            
            <br>
        </div>
    </div>
</div>
```

```css
.${{ id }}-modal-color,.${{ id }}-modal-hover:hover{color:#fff!important;background-color:${{ color }}!important}
```
