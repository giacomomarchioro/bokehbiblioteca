function table_to_csv(source) {
    const nrows = source.get_length()
    const selectedcolumns = ['numero_del_codice','titolo','Collocazione']
    const lines = [selectedcolumns.join(',')]
    for (let i = 0; i < nrows; i++) {
        let row = [];
        selectedcolumns.forEach(function (item, index) {
            row.push(source.data[item][i].toString());
          });
        lines.push(row.join(','))
    }
    return lines.join('\n').concat('\n')
}




const filename = 'oggetti_selezionati.csv'
const filetext = table_to_csv(source)
const blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' })

//addresses IE
if (navigator.msSaveBlob) {
    navigator.msSaveBlob(blob, filename)
} else {
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = filename
    link.target = '_blank'
    link.style.visibility = 'hidden'
    link.dispatchEvent(new MouseEvent('click'))
}
