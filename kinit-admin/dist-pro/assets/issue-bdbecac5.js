import{Y as s}from"./index-9da7d198.js";const a=a=>s.get({url:"/vadmin/help/issue/categorys",params:a}),e=a=>s.post({url:"/vadmin/help/issue/categorys",data:a}),i=a=>s.delete({url:"/vadmin/help/issue/categorys",data:a}),t=a=>s.put({url:`/vadmin/help/issue/categorys/${a.id}`,data:a}),l=a=>s.get({url:`/vadmin/help/issue/categorys/${a}`}),u=()=>s.get({url:"/vadmin/help/issue/categorys/options"}),d=a=>s.get({url:"/vadmin/help/issues",params:a}),r=a=>s.post({url:"/vadmin/help/issues",data:a}),p=a=>s.delete({url:"/vadmin/help/issues",data:a}),m=a=>s.put({url:`/vadmin/help/issues/${a.id}`,data:a}),n=a=>s.get({url:`/vadmin/help/issues/${a}`});export{u as a,r as b,n as c,p as d,l as e,a as f,d as g,i as h,e as i,t as j,m as p};