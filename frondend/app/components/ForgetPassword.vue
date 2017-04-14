<template>
<div>
    <el-form :model="form" :rules="rules" ref="form">
      <el-form-item label="手机号" :label-width="formLabelWidth" prop="user_name">
        <el-input v-model.number="form.user_name" auto-complete="off" key='user_name'></el-input>
      </el-form-item>
      <el-form-item label="验证码" :label-width="formLabelWidth" prop="verify_code">
        <el-input v-model="form.verify_code" auto-complete="off" class="verify-style" key='verify_code'></el-input>
        <el-button v-if="onLoading" type="primary" :loading="true" class="verifycode-button">{{loadingTime}}S后重发</el-button>
        <el-button v-else type="primary" v-on:click="get_verify_code" class="verifycode-button">获取验证码</el-button>
      </el-form-item>
      <el-form-item label="新密码" :label-width="formLabelWidth" prop="password">
        <el-input type="password" v-model="form.password" auto-complete="off" key='password'></el-input>
      </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
      <el-button @click="cancleForm">返回登录</el-button>
      <el-button type="primary" @click="submitForm">确定</el-button>
  </div>
 </div> 
</template>

<script>
  import {Message} from 'element-ui'
  import ApiRequest from '../common/ApiRequest.js'
  export default {
    props:["close"],
    data: function(){
      return {
        dialogVisible: false,
        loadingTime: '',
        onLoading: false,
        form: {
          user_name: '',
          verify_code: '',
          password: '',
        },
        rules:{
          user_name: [{ required:true, pattern: /^1[0-9]{10}$/, message:'请输入11位电话号码', trigger:'blur'}],
          verify_code:[{required:true, pattern: /^[0-9]{6}$/, message:'请输入6位验证码',trigger:'blur'}],
          password:[{ required:true, min:6, max:20, message:'密码长度6-20', trigger:'blur'}],
        },
        formLabelWidth: '120px'
      }
    },
    methods: {
      setLoading: function(){
        this.onLoading= true;
        let total = 60;
        this.loadingTime = total
        let self = this;
        let counter = setInterval(()=>{
          if(total==0){
            clearInterval(counter);
            this.onLoading= false;
          }else{
            self.loadingTime = total;
            total -= 1;
          }
        },1000)
      },
      get_verify_code: function(){
        this.$refs["form"].validateField('user_name',(valid)=>{
          if(valid!='请输入11位电话号码'){
            let url = 'user/verify_code_for_reset?mobile='+this.form.user_name;
            this.setLoading();
            ApiRequest.ajGet(url,(json) =>{
                if(json.success){
                  console.log(json.data);
                }else{  
                  Message.error({message:json.message,showClose:true});
                }
            })
          }else{
            return
          }
        });
      },
      submitForm: function(){
        this.$refs["form"].validate((valid) => {
          if(valid){
            let url = 'user/reset_password';
            let data = {
              mobile: this.form.user_name,
              verify_code: this.form.verify_code,
              password: this.form.password
            }
            let self = this;
            ApiRequest.ajPost(url, data, (json)=>{
              if(json.success){
                Message.success({message:'请用新密码登录',showClose:true})
                self.cancleForm()
              }else{
                Message.error({message:json.message,showClose:true});
              }
            })
          }else{
            return
          }
        })
      },
      cancleForm: function(){
        this.$refs["form"].resetFields();
        this.close();
      }
    }

  }
</script>
<style scoped>
  .verify-style{
    width:55%;
  }
  .verifycode-button{
    float: right;
  }
  .dialog-footer{
    text-align: right;
  }
</style>