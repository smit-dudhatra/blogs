# HTML Table Tags Hierarchy

```
table
├── caption
├── colgroup
│   └── col
├── thead
├── tbody
│   └── tr
│       ├── th
│       └── td
└── tfoot
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
| `<tbody>` | Groups the **body** rows |
| `<tfoot>` | Groups the **footer** rows |
| `<tr>` | Defines a **table row** (inside thead/tbody/tfoot) |
| `<th>` | **Header cell** — bold & centered by default |
| `<td>` | **Data cell** — regular content |

---

## 🔑 Key Points

- `thead`, `tbody`, and `tfoot` all can contain `<tr>` rows
- `<th>` and `<td>` are always **inside `<tr>`**
- `<caption>` is the **first child** of `<table>`
