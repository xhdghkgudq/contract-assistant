-- ==============================================
-- 合同分析系统 - contracts 表完整SQL脚本
-- MySQL版本
-- ==============================================

-- ------------------------------
-- 方案1: 向现有表添加新字段（推荐）
-- ------------------------------
USE contract_ai;

-- 添加新字段到contracts表
ALTER TABLE contracts
ADD COLUMN contract_number VARCHAR(100) COMMENT '合同编号' AFTER id,
ADD COLUMN party_a VARCHAR(255) COMMENT '甲方' AFTER contract_number,
ADD COLUMN party_b VARCHAR(255) COMMENT '乙方' AFTER party_a,
ADD COLUMN service_content TEXT COMMENT '服务内容' AFTER party_b,
ADD COLUMN service_period VARCHAR(255) COMMENT '服务期限' AFTER service_content,
ADD COLUMN service_fee VARCHAR(100) COMMENT '服务费用' AFTER service_period,
ADD COLUMN payment_method VARCHAR(255) COMMENT '支付方式' AFTER service_fee,
ADD COLUMN party_a_rights TEXT COMMENT '甲方权利义务' AFTER payment_method,
ADD COLUMN party_b_rights TEXT COMMENT '乙方权利义务' AFTER party_a_rights,
ADD COLUMN acceptance_standard TEXT COMMENT '验收标准' AFTER party_b_rights,
ADD COLUMN liability TEXT COMMENT '违约责任' AFTER acceptance_standard,
ADD COLUMN dispute_resolution TEXT COMMENT '争议解决' AFTER liability,
ADD COLUMN signing_date DATETIME COMMENT '签署日期' AFTER dispute_resolution,
ADD COLUMN result TEXT COMMENT '分析结果' AFTER signing_date,
ADD COLUMN subject_ok TINYINT(1) DEFAULT 0 COMMENT '主体明确' AFTER result,
ADD COLUMN object_clear TINYINT(1) DEFAULT 0 COMMENT '标的明确' AFTER subject_ok,
ADD COLUMN price_clear TINYINT(1) DEFAULT 0 COMMENT '价格明确' AFTER object_clear,
ADD COLUMN performable TINYINT(1) DEFAULT 0 COMMENT '可执行性' AFTER price_clear,
ADD COLUMN is_compliant TINYINT(1) DEFAULT 0 COMMENT '合规状态' AFTER performable,
ADD COLUMN is_void TINYINT(1) DEFAULT 0 COMMENT '是否作废' AFTER is_compliant;

-- ------------------------------
-- 方案2: 创建全新的contracts表（全新部署使用）
-- ------------------------------
-- DROP TABLE IF EXISTS contracts;
-- CREATE TABLE contracts (
--     id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
--     contract_number VARCHAR(100) COMMENT '合同编号',
--     party_a VARCHAR(255) COMMENT '甲方',
--     party_b VARCHAR(255) COMMENT '乙方',
--     service_content TEXT COMMENT '服务内容',
--     service_period VARCHAR(255) COMMENT '服务期限',
--     service_fee VARCHAR(100) COMMENT '服务费用',
--     payment_method VARCHAR(255) COMMENT '支付方式',
--     party_a_rights TEXT COMMENT '甲方权利义务',
--     party_b_rights TEXT COMMENT '乙方权利义务',
--     acceptance_standard TEXT COMMENT '验收标准',
--     liability TEXT COMMENT '违约责任',
--     dispute_resolution TEXT COMMENT '争议解决',
--     signing_date DATETIME COMMENT '签署日期',
--     content TEXT COMMENT '合同内容',
--     created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
--     expire_date DATETIME COMMENT '到期日期',
--     result TEXT COMMENT '分析结果',
--     subject_ok TINYINT(1) DEFAULT 0 COMMENT '主体明确',
--     object_clear TINYINT(1) DEFAULT 0 COMMENT '标的明确',
--     price_clear TINYINT(1) DEFAULT 0 COMMENT '价格明确',
--     performable TINYINT(1) DEFAULT 0 COMMENT '可执行性',
--     is_compliant TINYINT(1) DEFAULT 0 COMMENT '合规状态',
--     is_void TINYINT(1) DEFAULT 0 COMMENT '是否作废',
--     INDEX idx_contract_number (contract_number),
--     INDEX idx_party_a (party_a),
--     INDEX idx_party_b (party_b),
--     INDEX idx_expire_date (expire_date),
--     INDEX idx_is_void (is_void)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='合同表';

-- ------------------------------
-- 验证字段是否添加成功
-- ------------------------------
DESCRIBE contracts;
