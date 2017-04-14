<template>
  <el-col :span="20">
    <el-card class="card-content" :body-style="{ padding: '0px' }" v-for="item in menuData">
      <img :src="'/static/upload/'+item['url_address'][0]" class="image">
      <div class="content-text">
          <div>
            <span style="font-weight:700">{{item['name']}}</span>
            <span class="text-right">{{item['type']}}</span>
          </div>  
          <div>  
            <span style="color:red">{{item['price']}} 元/{{item['unit']}}</span>
            <span style="float:right">总共：{{item['quantity']}}份</span>
          </div>
          <div>
            <span>月销：{{item['monthly_sales']}}份</span>
            <span style="float:right">{{item['status']}}</span>
          </div>
          <div>  
            <el-button type="text" class="button" @click="modifyMenu(item)">编辑</el-button>
          </div>
      </div>
    </el-card>
  </el-col>
</template>

<script>
    import Vue from 'vue'
    import { Card,Message, Loading} from 'element-ui'
    import ApiRequest from '../common/ApiRequest.js'

    Vue.use(Card);
    
    export default {
      data:function() {
        return {
          menuData:[],
        }
      },
      created:function(){
        let that = this;
        let loadingInstance = Loading.service({text:'加载中......'});
        ApiRequest.ajGet('menu/get_all_menus',(json)=>{
            if(json.success){
                that.menuData = json.data;
                loadingInstance.close();
                if(json.data.length==0){
                  Message.info({message:'请添加菜单',showClose:true})
                }
            }else{
                loadingInstance.close();
                Message.error({message:json.message,showClose:true});
            }
        })
      },
      methods:{
        modifyMenu:function(itemData){
            this.$router.push({name: 'addMenu', params:{operation:'editMenu',item:itemData}})
        }
      }
    }
</script>

<style scoped>
.card-content {
    width: 200px;
    min-height: 220px;
    font-size: 14px;
    margin-left: 5px;
    margin-top: 5px;
    display: inline-block;
    border: 1px solid #d1dbe5;
    border-radius: 4px;
    background-color: #fff;
    overflow: hidden;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .12), 0 0 6px 0 rgba(0, 0, 0, .04)
}

.content-text {
    padding: 10px;
}

.text-right {
    float: right;
    color: #999
}

.button {
    padding: 0;
    float: right;
}

.image {
    width: 100%;
    height: 150px;
    display: block;
}

</style>