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
      },
      csseditor:'',
      cssoptions:{
        lineNumbers: true,
        line: true,
        tabSize: 2,
        mode: 'css',
        theme: 'material',
      },
      jseditor:'',
      jsoptions:{
        lineNumbers: true,
        line: true,
        tabSize: 2,
        mode: 'javascript',
        theme: 'material',
      },
    }
  },
  methods:{
    initeditor(){
      this.htmleditor = codemirror.fromTextArea(this.$refs.htmleditor, this.htmloptions);
      this.csseditor = codemirror.fromTextArea(this.$refs.csseditor, this.cssoptions);
      this.jseditor = codemirror.fromTextArea(this.$refs.jseditor, this.jsoptions);
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
