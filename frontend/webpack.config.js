//https://github.com/vuejs-templates/webpack/blob/master/template/build/webpack.prod.conf.js
var path = require('path');
var CopyWebpackPlugin = require('copy-webpack-plugin');
module.exports = {
    entry: {
        monitor: "./ts/monitor.ts",
    },
    output: {
        path: path.resolve(__dirname, './build/js'),
        filename: "[name].js",
    },
    resolve: {
        extensions: [".webpack.js", ".web.js", ".ts", ".tsx", ".js"],
    },
    module: {
        loaders: [
            { test: /\.tsx?$/, loader: "ts-loader" }
        ],
    },
    plugins: [
        new CopyWebpackPlugin([
            // {output}/file.txt
            { from: './css/*.css', to: path.resolve(__dirname, './build/css'), flatten: true },
        ]),
    ]
}
