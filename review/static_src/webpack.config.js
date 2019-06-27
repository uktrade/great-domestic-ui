const path = require('path');

module.exports = {
  entry: './src/main.js',
  externals: {
    annotator: 'annotator',
  },
  output: {
    path: path.resolve(__dirname, '../static/review'),
    filename: 'bundle.js',
    libraryTarget: 'umd',
    library: 'Review'
  }
};
