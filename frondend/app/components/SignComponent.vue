<template>
    <el-dialog size='tiny' :title="clickType=='sign_in' ? '登录':'注册'" v-model="dialogFormVisible" :tag="showTag">
        
        <el-form :model="form" :rules="clickType=='sign_in' ? rules1:rules2" :ref="clickType=='sign_in' ? 'sign_in_form':'sign_up_form'">
            <el-form-item label="用户名(手机号)" :label-width="formLabelWidth" prop="user_name">
              <el-input v-model.number="form.user_name" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item v-if="clickType=='sign_up'" label="验证码" :label-width="formLabelWidth" prop="verify_code">
              <el-input v-model.number="form.verify_code" auto-complete="off" class="verify-style"></el-input>
              <el-button type="primary" v-on:click="get_verify_code" class="verifycode-button">获取验证码</el-button>
            </el-form-item>
            <el-form-item label="密码" :label-width="formLabelWidth" prop="password1">
              <el-input type="password" v-model="form.password1" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item v-if="clickType=='sign_up'" label="确认密码" :label-width="formLabelWidth" prop="password2">
              <el-input type="password" v-model="form.password2" auto-complete="off"></el-input>
            </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button @click="cancleForm">取 消</el-button>
            <el-button type="primary" @click="submitForm">{{ clickType=='sign_in' ? '登录':'提交'}}</el-button>
        </div>
    </el-dialog>
</template>

<script>
    import ApiRequest from '../common/ApiRequest.js'
    module.exports = {
        props: ['showDialog','clickType'],
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
                    user_name: [{ type:'number',size:11,required:true, message:'请输入11位电话号码',trigger:'blur'}],
                    password1:[{ required:true, min:6,max:50,message:'密码长度6-20',trigger:'blur'}]
                },
                rules2:{
                    user_name: [{ type:'number',size:11,required:true, message:'请输入11位电话号码',trigger:'blur'}],
                    password1:[{ required:true, min:6,max:50,message:'密码长度6-20',trigger:'blur'}],
                    password2:[{ required:true, min:6,max:50,message:'密码长度6-20',trigger:'blur'}],
                    verify_code:[{type:'number',size:6,required:true, trigger:'blur'}]
                   
                }

            }
        },
        methods:{
            get_verify_code:function(){
                let url = 'user/get_verify_code?mobile='+this.sign_up_form.user_name;
                let patt=new RegExp('^[0-9]{11}$');
                let mobile = this.sign_up_form.user_name;
                if(!patt.test(mobile)){
                    alert('请输入11位电话号码');
                    return
                }
                ApiRequest.ajGet(url,(json) =>{
                    console.log(json)
                })
            },
            submitForm:function(){
                let form_name = this.clickType=='sign_in' ? 'sign_in_form':'sign_up_form';
                this.$refs[form_name].validate((valid) => {
                  if (valid) {
                    let data;
                    let url;

                    if (this.clickType=='sign_in'){
                        data = {
                            mobile:this.sign_in_form.user_name,
                            password1:this.sign_in_form.password1,
                        }
                        url = 'sign_in';
                        }
                    else{
                        data = {
                            mobile:this.sign_up_form.user_name,
                            password1:this.sign_up_form.password1,
                            password2:this.sign_up_form.password2,
                            verify_code:this.sign_up_form.verify_code
                        }
                        url = 'sign_up';
                    }

                    ApiRequest.ajPost(url,data,(json)=>{
                        console.log(json)
                    })
                  } else {
                    alert('error submit!!');
                    return false;
                  }
                });
            },
            cancleForm:function(){
                let form_name = this.clickType=='sign_in' ? 'sign_in_form':'sign_up_form';
                this.$refs[form_name].resetFields();
                this.dialogFormVisible=false
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
</style>