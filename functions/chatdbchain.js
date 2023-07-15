const chain = require("./chain.js");

module.exports = {
  call: async (query) => {
    const ch = await chain.chain();
    return await ch.call(query);
  },
};
