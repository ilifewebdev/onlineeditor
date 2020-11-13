<template>
<div class="editorwrap">
    <div class="left">
      <div class="editor">
        <div class="editorheader">HTML</div>
         <textarea ref="htmleditor"></textarea>
      </div>
      <div class="editor">
        <div class="editorheader">CSS</div>
         <textarea ref="csseditor"></textarea>
      </div>
      <div class="editor">
        <div class="editorheader">JavaScript</div>
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
import 'codemirror/mode/css/css';
import 'codemirror/mode/htmlmixed/htmlmixed';

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

export default {
  name: 'Home',
  data:function (){
    return{
      htmleditor:'',
      htmloptions:{
        lineNumbers: true,
        line: true,
        tabSize: 2,
        mode: 'htmlmixed',
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
      csseditor:'',
      cssoptions:{
        lineNumbers: true,
        line: true,
        tabSize: 2,
        mode: 'css',
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
      jseditor:'',
      jsoptions:{
        lineNumbers: true,
        line: true,
        tabSize: 2,
        mode: {name: "javascript", globalVars: true},
        theme: 'material',
        foldGutter: true,
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
        autoCloseBrackets: true,
        extraKeys: {"Ctrl-Q": function(cm){ cm.foldCode(cm.getCursor()) },"Ctrl-W": "autocomplete"},
        keyMap: "sublime",
      },

      htmlcontent:'',
      csscontent:'',
      jscontent:'',
    }
  },
  methods:{
    initeditor(){
      this.htmleditor = codemirror.fromTextArea(this.$refs.htmleditor, this.htmloptions);
      this.htmleditor.foldCode(codemirror.Pos(0, 0));

      this.htmleditor.on('change',_.debounce((editor) =>{
        this.htmlcontent = editor.getValue();
        console.log('html',this.htmlcontent);
        this.renderCode()
      },3000));


      this.csseditor = codemirror.fromTextArea(this.$refs.csseditor, this.cssoptions);
      this.csseditor.foldCode(codemirror.Pos(0, 0));
      this.csseditor.on('change',_.debounce((editor) =>{
        this.csscontent = editor.getValue();
        this.renderCode()
      },3000));

      this.jseditor = codemirror.fromTextArea(this.$refs.jseditor, this.jsoptions);
      this.jseditor.foldCode(codemirror.Pos(0, 0));
      this.jseditor.on('change',_.debounce((editor) =>{
        this.jscontent = editor.getValue();
        this.renderCode()
      },3000));
    },
    renderCode(){
      var html;

      if(this.jscontent != ''){
        html = this.htmlcontent + this.jscontent;
      }else{
        html = this.htmlcontent;
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
}


</style>