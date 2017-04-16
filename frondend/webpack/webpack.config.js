var path = require("path");
var webpack = require('webpack');

var CopyWebpackPlugin = require('copy-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var HtmlWebpackHarddiskPlugin = require('html-webpack-harddisk-plugin');

var mode = process.env.NODE_ENV;

if (mode === 'production') {
    baseUrl = "/static/"
} else {
    baseUrl = "http://localhost:8080/";
    // baseUrl = "http://192.168.31.113:8080/";
}

module.exports = {
    entry: {

      main:path.resolve(__dirname, '../app/main.js'),
      admin_panel:path.resolve(__dirname, '../app/admin_panel.js'),
      mobile_index:path.resolve(__dirname,'../mobile/mobile_index.js')
    },
    output: {
        path: path.resolve(__dirname, '../build'),
        filename: 'build/[name].js'
    },

    resolve: {
        alias: {
          'vue$': 'vue/dist/vue.common.js'
        },
        extensions: ['', '.js', '.jsx']
    },

    devtool: 'eval-source-map',
    
    plugins: [
      // new webpack.HotModuleReplacementPlugin(),
      new webpack.ProvidePlugin({
          'Promise': 'es6-promise', // Thanks Aaron (https://gist.github.com/Couto/b29676dd1ab8714a818f#gistcomment-1584602)
          'fetch': 'imports?this=>global!exports?global.fetch!whatwg-fetch'
      }),
      //把指定文件夹下的文件复制到指定的目录
      new HtmlWebpackPlugin({
        alwaysWriteToDisk: true,
        template: './frondend/index.html',
        filename: path.resolve(__dirname, '../../backend/templates/index.html'),
        inject: false,
        jspath:baseUrl+'build/main.js'
      }),
      new HtmlWebpackPlugin({
        alwaysWriteToDisk: true,
        template: './frondend/admin_panel.html',
        filename: path.resolve(__dirname, '../../backend/templates/admin_panel.html'),
        inject: false,
        jspath:baseUrl+'build/admin_panel.js'
      }),
      new HtmlWebpackPlugin({
        alwaysWriteToDisk: true,
        template: './frondend/mobile/mobile_index.html',
        filename: path.resolve(__dirname, '../../backend/templates/mobile_index.html'),
        inject: false,
        jspath:baseUrl+'build/mobile_index.js'
      }),
      new CopyWebpackPlugin(
        [{from:path.resolve(__dirname, '../build'),to:path.resolve(__dirname, '../../backend/static')}]
      ),
      new HtmlWebpackHarddiskPlugin()
    ],

    module: {
        loaders: [
        {
          test: /\.vue$/,
          loader: 'vue-loader'
        },
        {
          test: /\.js$/,
          loader: 'babel-loader',
          exclude: /node_modules/
        }, {
          test: /\.css$/,
          loader: 'style-loader!css-loader'
        }, {
          test: /\.less$/,
          loader: 'style-loader!css-loader!less-loader'
        },{
        test: /\.(eot|svg|ttf|woff|woff2)(\?\S*)?$/,
        loader: 'file-loader?publicPath='+baseUrl
      },
      {
        test: /\.(png|jpe?g|gif|svg)(\?\S*)?$/,
        loader: 'file-loader?publicPath='+baseUrl,
        query: {
          name: '[name].[ext]?[hash]'
        }
      }]
    },
    babel: {
     presets: ["es2015",'stage-0'],
     plugins: ['transform-runtime',["component", [
      {
        "libraryName": "element-ui",
        "styleLibraryName": "theme-default",
        "style": true
      }]]]
    },

    devServer: {
      contentBase: './frondend',
      outputPath: path.join(__dirname, '../../backend/static/'),
      color: true,
      historyApiFallback: true,
      inline: true,
      hot: true,
      debug: true,
      host:"0.0.0.0",
      headers: { "Access-Control-Allow-Origin": "*" }
  }
};

if (process.env.NODE_ENV === 'production') {
  module.exports.devtool = '#source-map'
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        warnings: false
      }
    }),
    // new webpack.LoaderOptionsPlugin({
    //   minimize: true
    // })
  ])
}