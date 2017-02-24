<template>  
  <el-col :span="20" class="left-nav-col">
    <div class="content">
      <div class="uploadArea">
        <label style="width: 80px" class="picture-label">图片</label>
        <div v-for="(item,index) in url_list" class="img-wrapper">
          <i class="el-icon-close" @click="handleRemovePicture(index)"></i>
          <img :src="item" class="upload-label"/>
        </div>
        <label @click="handleSelectPicture" class="upload-label">
          <i class="el-icon-plus"></i>
        </label>
        <input type="file" @change="handleChange" name="upload" class="upload-button" ref="input"/>
      </div>
      <br/>
      <el-form label-width="80px" :model="addMenuForm" ref="addMenuForm">
        <el-form-item label="菜名">
          <el-input v-model="addMenuForm.name"></el-input>
        </el-form-item>
        <el-form-item label="类别">
          <el-input v-model="addMenuForm.type"></el-input>
        </el-form-item>
        <el-form-item label="单位">
          <el-input v-model="addMenuForm.unit"></el-input>
        </el-form-item>
        <el-form-item label="单价">
          <el-input v-model="addMenuForm.price"></el-input>
        </el-form-item>
        <el-form-item label="数量">
          <el-input v-model="addMenuForm.quantity"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm">提交</el-button>
          <el-button @click="resetForm('addMenuForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </el-col>
</template>

<script>
  import Vue from 'vue'
  import { Form,Input,FormItem,Button,Upload,Dialog } from 'element-ui'
  import 'element-ui/lib/theme-default/upload.css'
  import ApiRequest from '../common/ApiRequest.js'

  let importList = [Form,Input,FormItem,Button,Upload,Dialog];
  for (let item in importList){
    Vue.use(importList[item])
  }

  let AddMenu={

    data:function () {
      return {
        url_list:[],
        upload_file_list:[],
        addMenuForm:{
          name:'',
          type:'',
          unit:'',
          price:'',
          quantity:''
        }
      }
    },

    methods:{
      handleSelectPicture:function () {
        this.$refs['input'].click()
      },
      handleRemovePicture:function(index){
        this.url_list.splice(index,1);
        this.upload_file_list.splice(index,1);
      },
      
      handleChange:function () {
        let that = this;
        if(this.$refs['input'].files.length == 1){
          let picture_file = this.$refs['input'].files[0];
          let pattern = new RegExp('^image\/\\w+','i');
          if (!pattern.test(picture_file.type)){
            return false
          }
          let reader = new FileReader();
          reader.readAsDataURL(picture_file);
          reader.onload = function (e) {
            let read_result = this.result;// or e.target.result
            that.url_list.push(read_result);
          };

          that.upload_file_list.push(picture_file);
        }
      },
      submitForm:function (form) {
        let data = {};
        for(let key in this.addMenuForm){
          data[key] = this.addMenuForm[key]
        }
        let files = this.upload_file_list;
        console.log(data,files);
        ApiRequest.ajUploadFile('upload/upload_file',{data:data,files:files},(json)=>{
          console.log(json);
        })
      }
    }
  }

  export default AddMenu
</script>

<style scoped>
  .content{
    width: 50%;
    margin-left: 5%;
    /*margin-top: 50px;*/
  }
  .upload-button{
    display: none;
  }
  .picture-label{
    text-align: right;
    vertical-align: middle;
    float: left;
    font-size: 14px;
    color: #48576a;
    padding: 11px 12px 11px 0;
    box-sizing: border-box;
    width: 80px;
    height: 148px;
    line-height: 148px;
  }
  .img-wrapper{
    display: inline-block;
  }
  .el-icon-close{
    display: inline-block;
    position: absolute;
    color: white;
    font-size: 16px;
    border-radius: 6px;
    background-color: #13cd66;  
  }

  .upload-label{
    background-color: #fbfdff;
    border: 1px dashed #c0ccda;
    border-radius: 6px;
    box-sizing: border-box;
    width: 148px;
    height: 148px;
    cursor: pointer;
    line-height: 146px;
    vertical-align: top;
    display: inline-block;
    text-align: center;
    margin: auto;
  }
  .el-icon-plus{
    font-size: 28px;
    color: #8c939d;
  }
</style>