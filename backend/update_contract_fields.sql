-- 合同分析系统 - 添加新字段SQL
-- 运行此脚本以向现有contracts表添加新字段

ALTER TABLE contracts 
ADD COLUMN contract_number VARCHAR(100) COMMENT '合同编号',
ADD COLUMN party_a VARCHAR(255) COMMENT '甲方',
ADD COLUMN party_b VARCHAR(255) COMMENT '乙方',
ADD COLUMN service_content TEXT COMMENT '服务内容',
ADD COLUMN service_period VARCHAR(255) COMMENT '服务期限',
ADD COLUMN service_fee VARCHAR(100) COMMENT '服务费用',
ADD COLUMN payment_method VARCHAR(255) COMMENT '支付方式',
ADD COLUMN party_a_rights TEXT COMMENT '甲方权利义务',
ADD COLUMN party_b_rights TEXT COMMENT '乙方权利义务',
ADD COLUMN acceptance_standard TEXT COMMENT '验收标准',
ADD COLUMN dispute_resolution TEXT COMMENT '争议解决',
ADD COLUMN signing_date DATETIME COMMENT '签署日期',
ADD COLUMN result TEXT,
ADD COLUMN subject_ok BOOLEAN DEFAULT FALSE,
ADD COLUMN object_clear BOOLEAN DEFAULT FALSE,
ADD COLUMN price_clear BOOLEAN DEFAULT FALSE,
ADD COLUMN performable BOOLEAN DEFAULT FALSE,
ADD COLUMN is_compliant BOOLEAN DEFAULT FALSE,
ADD COLUMN is_void BOOLEAN DEFAULT FALSE;

-- 如果需要删除旧的Review表关联字段（可选）
-- ALTER TABLE contracts DROP COLUMN review_id;
