<template>
    <el-dialog size='tiny' :title="showTitle()" v-model="dialogFormVisible" :tag="showTag">
        <forget-password v-if="showForget" :close="closeForget"></forget-password>
        <template v-else>
            <el-form :model="form" :rules="clickType=='sign_in' ? rules1:rules2" :ref="clickType=='sign_in' ? 'sign_in_form':'sign_up_form'">
                <el-form-item label="手机号" :label-width="formLabelWidth" prop="user_name">
                  <el-input v-model.number="form.user_name" auto-complete="off" key='user_name'></el-input>
                </el-form-item>
                <el-form-item v-if="clickType=='sign_up'" label="验证码" :label-width="formLabelWidth" prop="verify_code">
                  <el-input v-model="form.verify_code" auto-complete="off" class="verify-style" key='verify_code'></el-input>
                  <el-button type="primary" v-on:click="get_verify_code" class="verifycode-button">获取验证码</el-button>
                </el-form-item>
                <el-form-item label="密码" :label-width="formLabelWidth" prop="password1">
                  <el-input type="password" v-model="form.password1" auto-complete="off" key='password1'></el-input>
                </el-form-item>
                <el-form-item v-if="clickType=='sign_up'" label="确认密码" :label-width="formLabelWidth" prop="password2">
                  <el-input type="password" v-model="form.password2" auto-complete="off" key='password2'></el-input>
                </el-form-item>
            </el-form>
            <div v-if="clickType=='sign_in'" class='forget-password' @click="showForgetDialog">忘记密码</div>
            <div slot="footer" class="dialog-footer">
                <el-button @click="cancleForm">取 消</el-button>
                <el-button type="primary" @click="submitForm">{{ clickType=='sign_in' ? '登录':'提交'}}</el-button>
            </div>
        </template>
    </el-dialog>
    
</template>

<script>
    import ApiRequest from '../common/ApiRequest.js'
    import { Message } from 'element-ui'
    import ForgetPassword from './ForgetPassword.vue'

    module.exports = {
        props: ['showDialog','clickType'],
        components: {ForgetPassword},
        computed:{
            showTag:function(){
                
                if (this.checkStatus!=this.showDialog){
                    this.dialogFormVisible=true;
                    this.checkStatus=this.showDialog    
                }
                return this.showDialog
            },
            form:function(){
                    return this.clickType=='sign_in' ? this.sign_in_form:this.sign_up_form;
            }
        },
        data:function(){
            return{
                showForget: false,
                dialogFormVisible:false,
                checkStatus:false,
                sign_up_form:{
                    user_name:'',
                    verify_code:'',
                    password1:'',
                    password2:''
                },
                sign_in_form:{
                    user_name:'',
                    password1:''
                },
                
                formLabelWidth: '120px',

                // validate rules
                rules1:{
                    user_name: [{ required:true, pattern: /^1[0-9]{10}$/, message:'请输入11位电话号码',trigger:'blur'}],
                    password1:[{ required:true, min:6,max:20,message:'密码长度6-20',trigger:'blur'}]
                },
                rules2:{
                    user_name: [{ required:true, pattern: /^1[0-9]{10}$/, message:'请输入11位电话号码',trigger:'blur'}],
                    password1:[{ required:true, min:6,max:20,message:'密码长度6-20',trigger:'blur'}],
                    password2:[{ required:true, min:6,max:20,message:'密码长度6-20',trigger:'blur'}],
                    verify_code:[{required:true, pattern: /^[0-9]{6}$/, message:'请输入6位验证码',trigger:'blur'}]  
                },
                showForget: false
            }
        },
        methods:{
            get_verify_code:function(){
                let url = 'user/get_verify_code?mobile='+this.sign_up_form.user_name;
                ApiRequest.ajGet(url,(json) =>{
                    if(json.success){
                      console.log(json.data)  
                    }else{
                       Message.error({message:json.message,showClose:true})
                    }
                })
            },
            submitForm:function(){
                let form_name = this.clickType=='sign_in' ? 'sign_in_form':'sign_up_form';
                let self = this;
                this.$refs[form_name].validate((valid) => {
                  if (valid) {
                    let data;
                    let url;

                    if (self.clickType=='sign_in'){
                        data = {
                            mobile:self.sign_in_form.user_name,
                            password1:self.sign_in_form.password1,
                        }
                        url = 'sign_in';
                        }
                    else{
                        data = {
                            mobile:self.sign_up_form.user_name,
                            password1:self.sign_up_form.password1,
                            password2:self.sign_up_form.password2,
                            verify_code:self.sign_up_form.verify_code
                        }
                        url = 'sign_up';
                    }

                    ApiRequest.ajPost(url,data,(json)=>{
                        if(json.success){
                            let base_url = window.location.host;
                            window.location.href = '/'+json.redirect_url
                        }else{
                            Message.error({message:json.message,showClose:true})
                        }
                    })
                  } else {
                    return false;
                  }
                });
            },
            cancleForm:function(){
                let form_name = this.clickType=='sign_in' ? 'sign_in_form':'sign_up_form';
                this.$refs[form_name].resetFields();
                this.dialogFormVisible=false
            },
            showForgetDialog:function(){
               this.showForget = true;
            },
            closeForget:function(){
                this.showForget = false;
            },
            showTitle:function(){
                if(this.clickType == 'sign_in'){
                    return this.showForget ? '找回密码':'登录';    
                }
                else{
                    return '注册';
                }
                
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
    .forget-password{
        color: #20a0ff;
        cursor: pointer;
        width: 20%;
        float: right;
        text-align: right;
    }
</style>