CREATE TABLE `vadmin_suetactix_case_info` (
  `id` int(11) NOT NULL,
  `uniacid` int(11) NOT NULL DEFAULT '0',
  `name` varchar(100) NOT NULL DEFAULT '' COMMENT '案件名称',
  `info` text COMMENT '案件描述',
  `analysis` text NOT NULL COMMENT '案情研究',
  `timeline` varchar(2000) NOT NULL DEFAULT '' COMMENT '时间线',
  `relation` varchar(2000) NOT NULL DEFAULT '',COMMENT '逻辑关系',
  `cause` varchar(5000) NOT NULL DEFAULT '' COMMENT '案由',
  `claim` varchar(5000) NOT NULL DEFAULT '' COMMENT '诉讼请求',
  `questions` varchar(2000) NOT NULL DEFAULT '' COMMENT '待澄清问题',
  `createtime` int(11) NOT NULL DEFAULT '0',COMMENT '创建时间',
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,COMMENT '修改时间',
  `operator` varchar(20) NOT NULL,COMMENT '操作者',
  `cate_id` int(11) NOT NULL DEFAULT '0',COMMENT '案件类型',
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# 项目构建流程
1. 先描述行业场景, 明确需求
2. 找到对标业务流程, 分析关键节点
3. 确定核心功能, 明确关键参数与流程
4. 用kinit-api项目建立models ORM映射模型
5. 自动生成 schemas, params
6. 自动提取包类名
7. 根据核心功能和扩展流程需求,编写crud
8. 编写views路由
9. 编写前端 vue 页面和端口
10. 编写后端 nodejs 页面
11. 编写前端页面和端口
12. 编写操作文档
13. 单元测试
14. 打包部署


OPENAI_API_KEY = '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'  # tag=kinit
ZHIPU_API_KEY = ''