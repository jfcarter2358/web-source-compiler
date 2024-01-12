```yaml
id: foobar
header: Foobar
color: '#A3BE8C'
content: |
  <div class="card-container w3-container">
    <h2>Hello World!</h2>
  </div>
themes: 
  name: light
  base: theme-light
  border: theme-border-light
```

```html
<div class="w3-card-4 w3-round ${{ themes.name }} ${{ themes.base }} w3-border ${{ themes.border }}">
    <div class="w3-container ${{ id }}-card-color w3-round cascade-title">
        ${{ header }}
    </div>
    <div id="cascade-card" class="${{ themes.name }} ${{ themes.base }} card-overflow" width="100%" height="1000px">
        ${{ content }}
    </div>
</div>
```

```css
.${{ id }}-card-color,.${{ id }}-card-hover:hover{color:#fff!important;background-color:${{ color }}!important}
```
