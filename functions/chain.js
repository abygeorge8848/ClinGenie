const {OpenAI} = require("langchain/llms/openai");
const {SqlDatabase} = require("langchain/sql_db");
const {SqlDatabaseChain} = require("langchain/chains");

const {datasource} = require("./db.js");

module.exports = {
  chain: async () => {
    const db = await SqlDatabase.fromDataSourceParams({
      appDataSource: datasource,
    });
    const chain = new SqlDatabaseChain({
      llm: new OpenAI({
        openAIApiKey: "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",
        temperature: 0,
      }),
      database: db,
      sqlOutputKey: "sql",
      returnDirect: true,
      verbose: true,
      returnIntermediateSteps: true,
    });
    console.log('Issa me a mario : ', chain)
    //const stuff = {chain}
    return chain;
  },
};
