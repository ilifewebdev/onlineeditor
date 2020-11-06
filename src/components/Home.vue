<template>
    <textarea ref="editor"></textarea>
</template>

<script>

import 'codemirror/lib/codemirror.css';
import codemirror from "codemirror";

export default {
  name: 'Home',
  data:function (){
    return{
      editor:'',
      options:{
        lineNumbers: true,
        line: true,
        tabSize: 2,
      },
    }
  },
  methods:{
    initeditor(){
      this.editor = codemirror.fromTextArea(this.$refs.editor, this.options);
    }
  },
  mounted(){
    this.initeditor();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>
