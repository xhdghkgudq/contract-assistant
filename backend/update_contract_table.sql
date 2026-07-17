-- 合同分析系统 - contracts 表结构更新SQL

-- 1. 如果表已存在，先备份并重建（可选）
-- CREATE TABLE contracts_backup AS SELECT * FROM contracts;

-- 2. 添加新字段到现有表
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
ADD COLUMN liability TEXT COMMENT '违约责任',
ADD COLUMN dispute_resolution TEXT COMMENT '争议解决',
ADD COLUMN signing_date DATETIME COMMENT '签署日期',
ADD COLUMN result TEXT,
ADD COLUMN subject_ok BOOLEAN DEFAULT FALSE,
ADD COLUMN object_clear BOOLEAN DEFAULT FALSE,
ADD COLUMN price_clear BOOLEAN DEFAULT FALSE,
ADD COLUMN performable BOOLEAN DEFAULT FALSE,
ADD COLUMN is_compliant BOOLEAN DEFAULT FALSE,
ADD COLUMN is_void BOOLEAN DEFAULT FALSE;

-- 3. 如果需要创建新表（全新部署时使用）
/*
CREATE TABLE IF NOT EXISTS contracts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_number VARCHAR(100) COMMENT '合同编号',
    party_a VARCHAR(255) COMMENT '甲方',
    party_b VARCHAR(255) COMMENT '乙方',
    service_content TEXT COMMENT '服务内容',
    service_period VARCHAR(255) COMMENT '服务期限',
    service_fee VARCHAR(100) COMMENT '服务费用',
    payment_method VARCHAR(255) COMMENT '支付方式',
    party_a_rights TEXT COMMENT '甲方权利义务',
    party_b_rights TEXT COMMENT '乙方权利义务',
    acceptance_standard TEXT COMMENT '验收标准',
    liability TEXT COMMENT '违约责任',
    dispute_resolution TEXT COMMENT '争议解决',
    signing_date DATETIME COMMENT '签署日期',
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expire_date DATETIME,
    result TEXT,
    subject_ok BOOLEAN DEFAULT FALSE,
    object_clear BOOLEAN DEFAULT FALSE,
    price_clear BOOLEAN DEFAULT FALSE,
    performable BOOLEAN DEFAULT FALSE,
    is_compliant BOOLEAN DEFAULT FALSE,
    is_void BOOLEAN DEFAULT FALSE
);
*/

-- 4. 创建索引（可选，优化查询性能）
-- CREATE INDEX idx_contracts_contract_number ON contracts(contract_number);
-- CREATE INDEX idx_contracts_party_a ON contracts(party_a);
-- CREATE INDEX idx_contracts_party_b ON contracts(party_b);
-- CREATE INDEX idx_contracts_expire_date ON contracts(expire_date);
-- CREATE INDEX idx_contracts_signing_date ON contracts(signing_date);
