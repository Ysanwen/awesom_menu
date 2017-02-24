// 定义公共的异步请求方法

let base_url='api/';

module.exports = {
    ajGet:function (api_suffix,callback_function) {
        fetch(base_url+api_suffix,{
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            credentials: "same-origin"
        }).then((response)=>{
            return response.json()
        },(error)=>{
            alert(error.message)
        }).then((json)=>{
            callback_function(json)
        }).catch((ex)=>{
            console.log('parsing failed', ex)
        })
    },
    ajPost:function(api_suffix,post_data,callback_function){
        fetch(base_url+api_suffix,{
            method: 'post',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            credentials:'same-origin',
            body: JSON.stringify(post_data)
        }).then((response)=>{
            return response.json()
        },(error)=>{
            alert(error.message)
        }).then((json)=>{
            callback_function(json)
        }).catch((ex)=>{
            alert('parsing failed', ex)
        })
    },
    ajUploadFile:function(api_suffix,files_object,callback_function){
        
        let file_array = files_object.files ? files_object.files : [];
        let data_dict = files_object.data ? files_object.data:{};
        let data = new FormData();
        for (let item in file_array){
        
            data.append('files'+item.toString(),file_array[item])
        }
        for (let key in data_dict){
            data.append(key,data_dict[key])
        }
        fetch(base_url+api_suffix,{
            method:"POST",
            credentials:'same-origin',
            body:data
        }).then((response)=>{
            return response.json()
        },(error)=>{
            alert(error.message)
        }).then((json)=>{
            callback_function(json)
        }).catch((ex)=>{
            alert('parsing failed', ex)
        })
    }
}