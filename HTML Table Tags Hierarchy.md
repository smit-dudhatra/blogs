# HTML Table Tags Hierarchy

```
table
├── caption
├── colgroup
│   └── col
├── thead
│   └── tr
│       └── th
├── tbody
└── tfoot
    └── tr
        └── td
```

---

## 📝 Quick Explanation of Each Tag

| Tag | Description |
|---|---|
| `<table>` | Root element — wraps the entire table |
| `<caption>` | Title/description of the table |
| `<colgroup>` | Groups one or more columns for styling |
| `<col>` | Child of `<colgroup>` — defines individual column properties |
| `<thead>` | Groups the **header** rows |
| `<tbody>` | Groups the **body** rows (no direct children shown) |
| `<tfoot>` | Groups the **footer** rows |
| `<tr>` | Defines a **table row** (inside thead/tfoot) |
| `<th>` | **Header cell** — inside `<thead> > <tr>` |
| `<td>` | **Data cell** — inside `<tfoot> > <tr>` |

---

## 🔑 Key Points

- `<thead>` contains `<tr>` → `<th>` (header cells)
- `<tfoot>` contains `<tr>` → `<td>` (data cells)
- `<tbody>` is present but has no further children shown
- `<caption>` is always the **first child** of `<table>`
- `<col>` is always **inside `<colgroup>`**
- `rowspan` and `colspan` are attributes of **`<th>`** and **`<td>`** — used to merge cells across rows or columns
- `<col>` supports the **`style`** attribute — used to apply CSS styles to an entire column
