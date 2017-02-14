<template>
    <el-dialog :title="clickType=='sign_in' ? '登录':'注册'" v-model="dialogFormVisible" :class="showTag"">
        <el-form :model="form">
            <el-form-item label="用户名" :label-width="formLabelWidth">
              <el-input v-model="form.name" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="密码" :label-width="formLabelWidth">
              <el-input type="password" v-model="form.password1" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item v-if="clickType=='sign_up'" label="确认密码" :label-width="formLabelWidth">
              <el-input type="password" v-model="form.password2" auto-complete="off"></el-input>
            </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="dialogFormVisible = false">{{ clickType=='sign_in' ? '登录':'提交'}}</el-button>
        </div>
    </el-dialog>
</template>

<script>
            
    module.exports = {
        props: ['showDialog','clickType'],
        computed:{
            showTag:function(){
                
                if (this.checkStatus!=this.showDialog){
                    this.dialogFormVisible=true;
                    this.checkStatus=this.showDialog    
                }
                return this.showDialog
            }
        },
        data:function(){
            return{
                dialogFormVisible:false,
                checkStatus:false,
                form:{
                    name:''
                },
                formLabelWidth: '120px'
            }
        }
    }
</script>

<style scoped>
    p{
        text-align:center;
    }
</style>