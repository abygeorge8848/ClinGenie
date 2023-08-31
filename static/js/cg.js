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
        $("#dataTable").find('thead tr').append(`<th>${formatHeader(cols[i])}</th>`);
        colNames.push({ data: cols[i] });
    }
    return colNames;
  }

  const SQLfromLLMOutput = (llmOutput) => {
    // Pattern to match string between triple backticks
    const patternTripleBackticks = /```(.*?)```/s;
    const matchTripleBackticks = patternTripleBackticks.exec(llmOutput);
    if (matchTripleBackticks) {
      return matchTripleBackticks[1].trim();
    }
  
    // For the SQL Statement pattern, we'll replace newlines with spaces for better matching
    const cleanOutput = llmOutput.replaceAll("\n", " ");
  
    // Pattern to match string after "SQL Statement :"
    const patternSQLStatement = /SQL Statement\s?:\s?(.*?;)/;
    const matchSQLStatement = patternSQLStatement.exec(cleanOutput);
    if (matchSQLStatement) {
      return matchSQLStatement[1].trim();
    }
  
    return null;
  };
  
  
  
  

  const formatHeader = (header) => {
    //Replace _ with space, capitalize first letter
    return header.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());
  };

  function dispDate(date) {
    monArr=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    return date.substr(8,2)+" "+monArr[Number(date.substr(5,2))-1]+" "+date.substr(11,8)
  }
