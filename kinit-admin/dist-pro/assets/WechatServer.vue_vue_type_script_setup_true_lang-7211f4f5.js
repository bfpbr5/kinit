import{u as e,F as a}from"./useForm-ecbcdb43.js";import{e as s,W as t,M as o,x as r,N as p,a3 as l,r as n,P as i,dF as c,o as m,l as u,k as d,ai as _}from"./index-9da7d198.js";import{E as f}from"./el-button-8f21380c.js";import{u as w}from"./useValidator-e352e7a8.js";const v=s({__name:"WechatServer",props:{tabId:t.number},setup(s){const t=s,{required:v}=w(),x=o([{field:"wx_server_app_id",label:"AppID",colProps:{span:24},component:"Input",componentProps:{style:{width:"500px"}}},{field:"wx_server_app_secret",label:"AppSecret",colProps:{span:24},component:"Input",componentProps:{style:{width:"500px"}}},{field:"wx_server_email",label:"官方邮件",colProps:{span:24},component:"Input",componentProps:{style:{width:"500px"}}},{field:"wx_server_phone",label:"服务热线",colProps:{span:24},component:"Input",componentProps:{style:{width:"500px"}}},{field:"wx_server_site",label:"官方邮箱",colProps:{span:24},component:"Input",componentProps:{style:{width:"500px"}}},{field:"active",label:"",colProps:{span:24},formItemProps:{slots:{default:()=>r(l,null,[r(f,{loading:k.value,type:"primary",onClick:E},{default:()=>[p("立即提交")]})])}}}]),P=o({wx_server_app_id:[v()],wx_server_app_secret:[v()]}),{formRegister:b,formMethods:y}=e(),{setValues:h,getFormData:I,getElFormExpose:g}=y;let F=n({});const j=async()=>{const e=await _({tab_id:t.tabId});if(e){await h(e.data),F.value=e.data;const a=await g();null==a||a.clearValidate()}},k=n(!1),E=async()=>{const e=await g();if(await(null==e?void 0:e.validate())){const e=await I();if(k.value=!0,!e)return k.value=!1,i.error("未获取到数据");try{if(await c(e))return j(),i.success("更新成功")}finally{k.value=!1}}};return j(),(e,s)=>(m(),u(d(a),{rules:P,onRegister:d(b),schema:x},null,8,["rules","onRegister","schema"]))}});export{v as _};