<template>
<div class="editorwrap">
    <div class="left">
      <div class="editor">
        <div class="editorheader">
          <span>HTML</span>
          <label for="htmlmode">Mode</label>
          <select v-model="htmlmode">
            <option value="htmlmixed">htmlmixed</option>
            <option value="pug">pug</option>
          </select>
        </div>
         <textarea ref="htmleditor"></textarea>
      </div>
      <div class="editor">
        <div class="editorheader">
          <span>CSS</span>
          <label for="cssmode">Mode</label>
          <select v-model="cssmode">
            <option value="css">css</option>
            <option value="sass">sass</option>
          </select>
          <button @click="runcss()">运行</button>
        </div>
         <textarea ref="csseditor"></textarea>
      </div>
      <div class="editor">
        <div class="editorheader">
          <span>Javascript</span>
          <label for="jsmode">Mode</label>
          <select v-model="jsmode">
            <option value="javascript">javascript</option>
            <option value="coffeescript">coffeescript</option>
          </select>
          <button @click="runjs()">运行</button>
        </div>
         <textarea ref="jseditor"></textarea>
      </div>
    </div>
    <div class="right">
      <div class="editorheader">结果</div>
      <iframe class="iframe" ref="iframe" />
    </div>
  </div>
</template>

<script>

import 'codemirror/lib/codemirror.css';
import codemirror from "codemirror";

import 'codemirror/theme/material.css';
import 'codemirror/mode/javascript/javascript';
import 'codemirror/mode/coffeescript/coffeescript';

import 'codemirror/mode/css/css';
import 'codemirror/mode/sass/sass';
import 'codemirror/mode/htmlmixed/htmlmixed';
import 'codemirror/mode/pug/pug';

import 'codemirror/addon/fold/foldcode.js';
import 'codemirror/addon/fold/foldgutter.css';
import 'codemirror/addon/fold/foldgutter.js';
import 'codemirror/addon/fold/brace-fold.js';
import 'codemirror/addon/fold/xml-fold.js';
import 'codemirror/addon/fold/indent-fold.js';
import 'codemirror/addon/fold/markdown-fold.js';
import 'codemirror/addon/fold/comment-fold.js';

import 'codemirror/addon/edit/closebrackets.js';
import 'codemirror/addon/edit/closetag.js';
import 'codemirror/keymap/sublime.js';

import 'codemirror/addon/hint/show-hint.css';
import 'codemirror/addon/hint/show-hint.js';
import 'codemirror/addon/hint/css-hint.js';
import 'codemirror/addon/hint/html-hint.js';
import 'codemirror/addon/hint/javascript-hint.js';

import emmet from '@emmetio/codemirror-plugin';
emmet(codemirror);

import _ from 'lodash';

const pug = require('pug');
// const sass = require('sass');
import axios from 'axios';

export default {
  name: 'Home',
  data:function (){
    return{
      htmleditor:'',
      htmloptions:{
        lineNumbers: true,
        line: true,
        tabSize: 2,
        
        theme: 'material',
        foldGutter: true,
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
        autoCloseTags: true,
        autoCloseBrackets: true,
        
        extraKeys: {
        "Ctrl-Q": function(cm){ cm.foldCode(cm.getCursor()); },
        'Tab': 'emmetExpandAbbreviation',
        'Esc': 'emmetResetAbbreviation',
        'Enter': 'emmetInsertLineBreak'
        }
      },
      htmlmode:'htmlmixed',

      csseditor:'',
      cssoptions:{
        lineNumbers: true,
        line: true,
        tabSize: 2,
        theme: 'material',
        foldGutter: true,
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
        autoCloseBrackets: true,
        
        extraKeys: {
        "Ctrl-Q": function(cm){ cm.foldCode(cm.getCursor()); },
        'Tab': 'emmetExpandAbbreviation',
        'Esc': 'emmetResetAbbreviation',
        'Enter': 'emmetInsertLineBreak'
        }
      },
      cssmode:'css',

      jseditor:'',
      jsoptions:{
        lineNumbers: true,
        line: true,
        tabSize: 2,
      
        theme: 'material',
        foldGutter: true,
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
        autoCloseBrackets: true,
        extraKeys: {"Ctrl-Q": function(cm){ cm.foldCode(cm.getCursor()) },"Ctrl-W": "autocomplete"},
        keyMap: "sublime",
      },
      jsmode:'javascript',

      htmlcontent:'',
      csscontent:'',
      jscontent:'',
    }
  },
  watch:{
    htmlmode() {
      this.htmleditor.setOption("mode", this.htmlmode);
    },
    cssmode() {
      this.csseditor.setOption("mode", this.cssmode);
    },
    jsmode() {
      this.jseditor.setOption("mode", this.jsmode);
    },
  },
  methods:{
    initeditor(){
      this.htmleditor = codemirror.fromTextArea(this.$refs.htmleditor, Object.assign(this.htmloptions, {mode: this.htmlmode}));
      this.htmleditor.foldCode(codemirror.Pos(0, 0));
      this.htmleditor.on('change',_.debounce((editor) =>{
        this.htmlcontent = editor.getValue();
        this.renderCode();
      },1000));

      console.log('css',Object.assign(this.cssoptions, {mode: this.cssmode}));
      this.csseditor = codemirror.fromTextArea(this.$refs.csseditor,Object.assign(this.cssoptions, {mode: this.cssmode}));
      this.csseditor.foldCode(codemirror.Pos(0, 0));
      this.csseditor.on('change',_.debounce((editor) =>{
        this.csscontent = editor.getValue();
        if(this.cssmode == 'css'){
          this.renderCode()
        }
        
      },1000));

      this.jseditor = codemirror.fromTextArea(this.$refs.jseditor,Object.assign(this.jsoptions, {mode: this.jsmode}));
      this.jseditor.foldCode(codemirror.Pos(0, 0));
      this.jseditor.on('change',_.debounce((editor) =>{
        this.jscontent = editor.getValue();
        if(this.jsmode == 'javascript'){
          this.renderCode()
        }
      },1000));
    },
    compilehtml(){
      if(this.htmlmode == 'pug'){
        return pug.render(this.htmlcontent);
      }else{
        return this.htmlcontent;
      }
    },
   
    runcss(){
      axios.post('/api/scss', {
      scss: this.csscontent,
      })
      .then((res) => {
        this.csscontent = res.data;
        this.renderCode();
      })
      .catch((err)=> {
        console.log(err);
      });
    },
    runjs(){
      axios.post('/api/js', {
      js: this.jscontent,
      })
      .then((res) => {
        this.jscontent= res.data;
        console.log('js',this.jscontent);
        this.renderCode();
      })
      .catch((err)=> {
        console.log(err);
      });
    },

    renderCode(){
      var html;
      if(this.jscontent != ''){
        html = this.compilehtml(this.htmlcontent) + this.jscontent;
      }else{
        html = this.compilehtml(this.htmlcontent);
      } 
      let css = this.csscontent;
      const iframe = this.$refs.iframe;
      console.log('iframe',this.jscontent,html);
      const document = iframe.contentDocument;
      const documentContents = `
          <!DOCTYPE html>
          <html lang="en">
          <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>Document</title>
            <style>
              ${css}
            </style>
          </head>
          <body>
            ${html}
          </body>
          </html>
        `;

      document.open();
      document.write(documentContents);
      document.close();
    }
  },
  mounted(){
    this.initeditor();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

.editorwrap{
  display: flex;
  width: 100%;
  height: 100vh;
  .left,.right{
    flex:1;
    height: 100%;
  }
  .left{
    display: flex;
    flex-direction: column;
  }
  .editor{
    flex:1;
  }
  .editorheader{
    height: 30px;
    background-color:#808080;
    color:#fff;
    display: flex;
    align-items: center;
    padding-left: 20px;
  }
  .iframe{
    width: 100%;
    height: 100%;
  }
  span{
    display: inline-block;
    margin-right: 10px;
  }
}


</style>