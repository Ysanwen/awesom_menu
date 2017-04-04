<template>
<div>
    <el-form :model="form" :rules="rules" ref="form">
      <el-form-item label="手机号" :label-width="formLabelWidth" prop="user_name">
        <el-input v-model.number="form.user_name" auto-complete="off" key='user_name'></el-input>
      </el-form-item>
      <el-form-item label="验证码" :label-width="formLabelWidth" prop="verify_code">
        <el-input v-model.number="form.verify_code" auto-complete="off" class="verify-style" key='verify_code'></el-input>
        <el-button type="primary" v-on:click="get_verify_code" class="verifycode-button">获取验证码</el-button>
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
  export default {
    props:["close"],
    data: function(){
      return {
        dialogVisible: false,
        form: {
          user_name: '',
          verify_code: '',
          password: '',
        },
        rules:{
          user_name: [{ type:'number',size:11,required:true, message:'请输入11位电话号码',trigger:'blur'}],
          verify_code:[{type:'number',size:6,required:true, trigger:'blur'}],
          password:[{ required:true, min:6,max:50,message:'密码长度6-20',trigger:'blur'}],
        },
        formLabelWidth: '120px'
      }
    },
    methods: {
      get_verify_code: function(){
        return
      },
      submitForm: function(){
        return
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