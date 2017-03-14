<template>
    <div>
        <div class="food-img"><img :src='"/static/upload/"+item.url_address[0]'></div>
        <div class="food-content">
          <p class="food-title">{{ item.name }}</p>
          <p class="food-type">分类：{{ item.type }}</p>
          <p class="food-quantity">今日供应：{{ item.quantity }}<br/>月销量：3000</p>
          <div class="food-bottom">
          <p class="food-price">¥{{ item.price }}</p>
          <!-- <i class="material-icons remove-icon" @click="reduceQuantity">remove_circle</i> -->
          <span class="material-icons remove-icon" @click="reduceQuantity" :style="showOrder ? hideIcon:showIcon">
              <svg width="24" height="24" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">
             <g>
              <title>remove_circle</title>
              <ellipse fill="#3190e8" stroke-width="null" stroke-dasharray="null" stroke-linejoin="null" stroke-linecap="null" cx="12" cy="12" id="svg_0" rx="10" ry="10" stroke="#3190e8"/>
              <rect fill="#ffffff" stroke-width="null" stroke-dasharray="null" stroke-linejoin="null" stroke-linecap="null" x="6" y="11" width="12" height="2" id="svg_1" stroke="#ffffff"/>
             </g>

            </svg>
          </span>
          <span class="order-number" :style="showOrder ? marginBig:marginSmall">{{ showOrder ? '数量：' : ''}}{{ quantity  }}</span>
          <!-- <i class="material-icons add-icon" @click="addQuantity">add_circle</i> -->
          <span class="material-icons add-icon" @click="addQuantity" :style="showOrder ? hideIcon:showIcon">
            <svg width="24" height="24" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">
             <g>
              <title>add_circle</title>
              <ellipse fill="#3190e8" stroke-width="null" stroke-dasharray="null" stroke-linejoin="null" stroke-linecap="null" cx="12" cy="12" id="svg_3" rx="10" ry="10" stroke="#3190e8"/>
              <rect fill="#ffffff" stroke-width="null" stroke-dasharray="null" stroke-linejoin="null" stroke-linecap="null" x="6" y="11" width="12" height="2" id="svg_4" stroke="#ffffff"/>
              <rect fill="#ffffff" stroke-width="null" stroke-dasharray="null" stroke-linejoin="null" stroke-linecap="null" x="6" y="11" width="12" height="2" stroke="#ffffff" id="svg_5" transform="rotate(90, 12, 12)"/>
             </g>

            </svg>
          </span>
          </div>
        </div>
    </div>    
</template>

<script>
import 'mint-ui/lib/style.css'
    export default {
        data:function(){
            return{
                quantity:this.defaultQuantity,
                showIcon:{display:'inline-block'},
                hideIcon:{display:'none'},
                marginBig:{marginLeft:'5rem',fontSize:'14px',width:'5rem'},
                marginSmall:{marginLeft:'0.5rem',fontSize:'22px',width:'0.5rem'}
            }
        },
        props:['item','defaultQuantity'],
        computed:{
            showOrder:function(){
                return this.$store.state.showOrder;
            },
        },
        methods:{
            reduceQuantity:function(){
                if(this.quantity>0){
                    this.quantity-=1;
                    // call the action function defined in store.js
                    this.$store.dispatch('reduceItem',this.item);
                }
            },
            addQuantity:function(){
                this.quantity+=1;
                // // call the action function defined in store.js
                this.$store.dispatch('addItem',this.item);
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