<template>
    <div>
        <div class="food-img"><img :src='"/static/upload/"+item.url_address[0]'></div>
        <div class="food-content">
          <p class="food-title">{{ item.name }}</p>
          <p class="food-type">分类：{{ item.type }}</p>
          <p class="food-quantity">今日供应：{{ item.quantity }}<br/>月销量：3000</p>
          <div class="food-bottom">
          <p class="food-price">¥{{ item.price }}</p>
          <i class="material-icons remove-icon" @click="reduceQuantity">remove_circle</i>
          <span class="order-number">{{ quantity  }}</span>
          <i class="material-icons add-icon" @click="addQuantity">add_circle</i>
          </div>
        </div>
    </div>    
</template>

<script>
    export default {
        data:function () {
            return{
                quantity:0
            }
        },
        props:['item'],
        methods:{
            reduceQuantity:function(){
                if(this.quantity>0){
                    this.quantity-=1;
                    this.$emit('reduce',this.item,1);
                }
            },
            addQuantity:function(){
                this.quantity+=1;
                this.$emit('add',this.item,1);
            }
        }
    }   
</script>

<style scoped>
    .food-img{
        width: 40%;
        height: 6rem;
        display: inline-block;
        float: left;
        
    }
    .food-img img{
        width: 100%;
        height: 100%;
    }
    .food-content{
        display: inline-block;
        height: 6rem;
        margin: auto;
        width: 58%;
        padding-left: 5px;
        line-height: 1rem;
        font-size: 12px;
    }
    .food-content p{
        padding: 0px;
        margin: auto;
    }
    .food-title{
        font-weight: 700;
        line-height: 1.5rem;
        height: 1.5rem;
    }
    .food-type{                
        color: #999;
    }
    .food-price{
        line-height: 1.5rem;
        color: red;
        height: 1.5rem;
        font-size: 14px;
        font-weight: 700;
        display: inline-block;
        float: left
    }
    .material-icons{
        color: rgba(49, 144, 232,1);
    }
    .remove-icon{
        margin-left: 3rem;
    }
    .order-number{
        width: 1.5rem;
        height: 1.5rem;
        display: inline-block;
        font-size: 22px;
        position: absolute;
        line-height: 1.5rem;
        margin-left: 0.5rem
    }
    .add-icon{
        margin-left: 2rem;
    }
</style>