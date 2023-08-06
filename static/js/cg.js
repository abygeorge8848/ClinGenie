function dtFormatData(data, cols) {
    const retval = [];
    for (const row of data) {
      const object = {}; 
      var colIndex = 0;
      for (const val of row) {
        const key = cols[colIndex++]
        object[key] = val;
      }
      retval.push(object);
    }
    return retval;
  }

  function dtFormatCols(cols) {
    var colNames = [];
    for (let i = 0; i < cols.length; i++) {
        $("#dataTable").find('thead tr').append(`<th>${cols[i]}</th>`);
        colNames.push({ data: cols[i] });
    }
    return colNames;
  }

  const SQLfromLLMOutput = (llmOutput) => {
    const pattern = /```(.*?)```/;
    const match = pattern.exec(llmOutput);
    if (match) {
      return match[1];
    } else {
      return null;
    }
  };