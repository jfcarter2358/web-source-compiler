```yaml
title: My First WSC Page
color: '#FA7538'
themes:
    name: light
    base: theme-light
    border: theme-border-light
    text: theme-text
    table: theme-border-light
    hover: theme-hover-text-dark
```

```py
import jfcarter2358.page
import jfcarter2358.card
import jfcarter2358.appearance
```

```html
<jfcarter2358.appearance>
</jfcarter2358.appearance>
<jfcarter2358.page>
title: ${{ title }}
color: "${{ color }}"
content: |
  <jfcarter2358.card>
    id: main-card
    header: <h1>Hello World!</h1>
    color: "${{ color }}"
    content: |
      <h1>Card contents!</h1>
    themes:
      name: ${{ themes.name }}
      base: ${{ themes.base }}
      border: ${{ themes.border }}
  </jfcarter2358.card>
themes: 
  name: ${{ themes.name }}
  base: ${{ themes.base }}
  border: ${{ themes.border }}
  text: ${{ themes.text }}
  table: ${{ themes.table }}
  hover: ${{ themes.hover }}
</jfcarter2358.page>
```


