<template>  
  <el-col :span="20" class="left-nav-col">
    <div class="content">
      <div class="uploadArea">
        <label style="width: 80px" class="picture-label">图片</label>
        <div v-for="(item,index) in url_list" class="img-wrapper">
          <i class="el-icon-close" @click="handleRemovePicture(index)"></i>
          <img :src="createLink(item)" class="upload-label"/>
        </div>
        <label @click="handleSelectPicture" class="upload-label">
          <i class="el-icon-plus"></i>
        </label>
        <input type="file" @change="handleChange" name="upload" class="upload-button" ref="input"/>
      </div>
      <br/>
      <el-form label-width="80px" :model="addMenuForm" ref="addMenuForm" :rules="validateRules">
        <el-form-item label="菜名" prop="name">
          <el-input v-model="addMenuForm.name" placeholder="菜品名称"></el-input>
        </el-form-item>
        <el-form-item label="类别" prop="type">
          <el-input v-model="addMenuForm.type" placeholder="主食、小炒、酒水、饮料等"></el-input>
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-input v-model="addMenuForm.unit" placeholder="份、杯"></el-input>
        </el-form-item>
        <el-form-item label="单价" prop="price">
          <el-input v-model.number="addMenuForm.price" placeholder="每份的价格"></el-input>
        </el-form-item>
        <el-form-item label="数量" prop="quantity">
          <el-input v-model.number="addMenuForm.quantity" placeholder="每日供应数量"></el-input>
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-select v-model="addMenuForm.status" placeholder="请选择是否上架">
            <el-option label="立即上架" value="0"></el-option>
            <el-option label="暂不上架" value="1"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm">提交</el-button>
          <el-button v-if="operation == 'editMenu'" @click="cancelEdit">取消</el-button>
          <el-button v-else @click="resetForm('addMenuForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </el-col>
</template>

<script>
  import Vue from 'vue'
  import { Form,Input,FormItem,Button,Upload,Dialog,Select,Option } from 'element-ui'
  import { Message } from 'element-ui'
  import ApiRequest from '../common/ApiRequest.js'

  let importList = [Form,Input,FormItem,Button,Upload,Dialog,Select,Option];
  for (let item in importList){
    Vue.use(importList[item])
  }

  let AddMenu={

    data:function () {
      return {
        url_list:[],
        url_list_len:0,
        upload_file_list:[],
        operation:'addMenu',
        addMenuForm:{
          name:'',
          type:'',
          unit:'',
          price:'',
          quantity:'',
          status:'0'
        },
        validateRules:{
          name:[{required:true, message: '请输入菜名', trigger: 'blur'}],
          type:[{required:true, message: '请输入类别', trigger: 'blur'}],
          unit:[{required:true, message: '请输入计费单位', trigger: 'blur'}],
          price:[{required:true, type:'number', message: '请输入单价', trigger: 'blur'}],
          quantity:[{required:true, type:'number', message: '请输入数量', trigger: 'blur'}],
          status:[{required:true}]
        }
      }
    },
    created: function(){
      let operation = this.$route.params.operation;
      this.operation = operation;
      if(operation === 'editMenu'){
        let item = this.$route.params.item;
        item['status'] = item['status'] === '热销中' ? '0' : '1';
        this.addMenuForm = item;
        this.url_list = item['url_address'];
        this.url_list_len = item['url_address'].length;
      }
    },
    methods:{
      handleSelectPicture:function () {
        this.$refs['input'].click()
      },
      handleRemovePicture:function(index){
        if(this.operation === 'addMenu'){
          this.url_list.splice(index,1);
          this.upload_file_list.splice(index,1);
        }
        if(this.operation === 'editMenu'){
          let remove_item = this.url_list[index];
          if(remove_item.indexOf('data') === -1){
            this.url_list.splice(index,1);
            this.url_list_len -= 1;
          }
          else{
            this.url_list.splice(index,1);
            this.upload_file_list.splice(index-this.url_list_len, 1);
          }
        }
      },
      createLink:function(link){
        let url;
        if(link.indexOf('data') === -1){
          url = '/static/upload/' + link; 
        }
        else{
          url = link;
        }
        return url
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
        }else {
          Message.alert('no picture selected');
        }
      },
      submitForm:function(){
        if(this.operation === 'addMenu'){
          this.submitAdd();
        }
        if(this.operation === 'editMenu'){
          this.submitEdit();
        }
      },
      submitAdd:function () {
        let that = this;
        this.$refs['addMenuForm'].validate((valid)=>{
          if(valid){
            let data = {};
            for(let key in that.addMenuForm){
              data[key] = that.addMenuForm[key]
            }
            let files = that.upload_file_list;
            if(files.length <=0){
              Message.error('请选择图片');
              return
            }
            
            ApiRequest.ajUploadFile('upload/upload_file',{data:data,files:files},(json)=>{
              if(json.success){
                that.$refs['addMenuForm'].resetFields();
                for(let item in that.upload_file_list){
                  that.handleRemovePicture(item);
                }
                that.upload_file_list = [];
                Message.success('创建成功！');
              }
              else{
                Message.error(json.message);
              }
            })
          }
          else{
            Message.error('请填写表单！')
          }
        })
          
      },
      submitEdit: function(){
        let menu_id = this.$route.params.item.id;
        let new_url_list = this.url_list.filter((item)=>{if(item.indexOf('data')===-1){return item}});
        let files = this.upload_file_list;
        let data = this.addMenuForm;
        if(new_url_list.lenght<=0 && files.length<=0){
          Message.error('请选择图片');
          return
        }
        let that = this;
        this.$refs['addMenuForm'].validate((valid)=>{
          if(valid){
            data['new_url_list'] = JSON.stringify(new_url_list);
            ApiRequest.ajUploadFile('menu/update_menu',{data:data,files:files},(json)=>{
              if(json.success){
                Message.success('跟新成功');
                that.$router.push({'path':'/allMenu'})
              }
              else{
                Message.error('跟新失败')
              }
            })
          }
          else{
            Message.error('请填写表单！')
          }
        })
      },
      cancelEdit: function(){
        this.$router.push({'path':'/allMenu'})
      },
      resetForm:function(){
        this.$refs['addMenuForm'].resetFields();
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