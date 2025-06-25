"""
不动产自助查询一体机 - 核心配置管理
"""

from pydantic_settings import BaseSettings
from typing import Optional, List
import os
from pathlib import Path


class Settings(BaseSettings):
    """应用设置配置类"""

    # ===== 应用基础配置 =====
    APP_NAME: str = "不动产自助查询一体机"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # ===== 服务器配置 =====
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1

    # ===== 数据库配置 =====
    # SQLite配置（开发环境）
    # DATABASE_URL: str = "sqlite:///./data/kiosk.db"

    # MySQL配置（推荐生产环境）
    DATABASE_URL: str = (
        "mysql+aiomysql://kiosk_user:kiosk_password@localhost:3306/real_estate_kiosk?charset=utf8mb4"
    )
    DATABASE_ECHO: bool = False

    # MySQL连接池配置
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 3600

    # ===== 安全配置 =====
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # RSA加密配置
    RSA_PRIVATE_KEY_PATH: str = "./keys/rsa_private.pem"
    RSA_PUBLIC_KEY_PATH: str = "./keys/rsa_public.pem"
    RSA_KEY_SIZE: int = 2048

    # SM2加密配置（国密）
    SM2_PRIVATE_KEY: str = ""
    SM2_PUBLIC_KEY: str = ""

    # ===== 硬件设备配置 =====

    # 身份证读卡器 - 新中新F200
    ID_CARD_READER_ENABLED: bool = True
    ID_CARD_READER_TYPE: str = "XZX_F200"
    ID_CARD_READER_SDK_PATH: str = "/opt/xinzhongxin/lib/libIDCardReader.so"
    ID_CARD_READER_TIMEOUT: int = 10

    # 双目摄像头 - 健德源JDY-K2002R
    CAMERA_ENABLED: bool = True
    CAMERA_TYPE: str = "JDY_K2002R"
    CAMERA_INDEX_LEFT: int = 0
    CAMERA_INDEX_RIGHT: int = 1
    CAMERA_WIDTH: int = 1920
    CAMERA_HEIGHT: int = 1080
    CAMERA_FPS: int = 30

    # 人脸识别 - 虹软SDK
    FACE_RECOGNITION_ENABLED: bool = True
    ARCFACE_SDK_PATH: str = "/opt/arcsoft/lib/"
    ARCFACE_APP_ID: str = ""
    ARCFACE_SDK_KEY: str = ""
    ARCFACE_THRESHOLD: float = 0.85  # 人脸相似度阈值
    LIVENESS_THRESHOLD: float = 0.7  # 活体检测阈值

    # 打印机配置 - 惠普HP454DW
    PRINTER_ENABLED: bool = True
    PRINTER_NAME: str = "HP_LaserJet_Pro_454DW"
    PRINTER_IP: Optional[str] = None
    CUPS_SERVER: str = "localhost:631"
    DEFAULT_PAPER_SIZE: str = "A4"
    PRINT_QUALITY: str = "normal"  # draft, normal, high

    # 盖章机配置 - 汉威信GZ820
    STAMP_MACHINE_ENABLED: bool = True
    STAMP_DEVICE_PORT: str = "/dev/ttyS0"
    STAMP_DEVICE_BAUDRATE: int = 9600
    STAMP_DEVICE_TIMEOUT: int = 5
    STAMP_PRESSURE: int = 80  # 盖章压力 0-100

    # 二维码扫描仪 - 新大陆NLS-FM25-EX
    QR_SCANNER_ENABLED: bool = True
    QR_SCANNER_PORT: str = "/dev/ttyUSB0"
    QR_SCANNER_BAUDRATE: int = 115200
    QR_SCANNER_TIMEOUT: int = 3

    # UPS配置 - 山特MT-500Pro
    UPS_ENABLED: bool = True
    UPS_DEVICE_PORT: str = "/dev/ttyUSB1"
    UPS_MONITOR_INTERVAL: int = 30
    UPS_LOW_BATTERY_THRESHOLD: int = 20  # 低电量告警阈值

    # 补光灯控制
    LED_LIGHT_ENABLED: bool = True
    LED_CONTROL_TYPE: str = "RS232"
    LED_CONTROL_PORT: str = "/dev/ttyUSB2"
    LED_AUTO_BRIGHTNESS: bool = True
    LED_DEFAULT_BRIGHTNESS: int = 80  # 默认亮度 0-100

    # ===== 业务接口配置 =====

    # 政务查询接口
    GOVERNMENT_API_ENABLED: bool = True
    GOVERNMENT_API_BASE_URL: str = "https://api.realestate.gov.cn"
    GOVERNMENT_API_KEY: str = ""
    GOVERNMENT_API_SECRET: str = ""
    GOVERNMENT_API_TIMEOUT: int = 30
    GOVERNMENT_API_RETRY_TIMES: int = 3

    # 身份认证接口
    ID_VERIFY_API_URL: str = "https://id.verify.gov.cn"
    ID_VERIFY_API_KEY: str = ""

    # ===== 文件存储配置 =====

    # 临时文件目录
    TEMP_FILE_PATH: str = "/tmp/kiosk_temp"
    TEMP_FILE_EXPIRE_HOURS: int = 24

    # 输出文件目录
    OUTPUT_FILE_PATH: str = "/opt/kiosk/output"

    # 日志文件目录
    LOG_FILE_PATH: str = "/var/log/kiosk"
    LOG_LEVEL: str = "INFO"
    LOG_RETENTION_DAYS: int = 30

    # 数据备份目录
    BACKUP_PATH: str = "/opt/kiosk/backup"
    BACKUP_INTERVAL_HOURS: int = 24

    # ===== 音频配置 =====

    # TTS语音配置
    TTS_ENABLED: bool = True
    TTS_ENGINE: str = "espeak"  # espeak, festival, pyttsx3
    TTS_LANGUAGE: str = "zh-cn"
    TTS_SPEED: int = 150  # 语速
    TTS_VOLUME: float = 0.8  # 音量 0.0-1.0
    AUDIO_OUTPUT_DEVICE: str = "default"

    # ===== 触摸屏配置 =====

    # 显示配置
    SCREEN_WIDTH: int = 1920
    SCREEN_HEIGHT: int = 1080
    SCREEN_ORIENTATION: str = "landscape"  # landscape, portrait

    # 触控配置
    TOUCHSCREEN_ENABLED: bool = True
    TOUCHSCREEN_DEVICE: str = "/dev/input/event0"
    TOUCH_CALIBRATION: bool = True

    # ===== 系统监控配置 =====

    # 设备状态监控
    DEVICE_CHECK_INTERVAL: int = 10  # 秒
    DEVICE_TIMEOUT: int = 5  # 设备响应超时

    # 系统资源监控
    CPU_ALERT_THRESHOLD: int = 85  # CPU使用率告警阈值
    MEMORY_ALERT_THRESHOLD: int = 85  # 内存使用率告警阈值
    DISK_ALERT_THRESHOLD: int = 90  # 磁盘使用率告警阈值

    # 网络监控
    NETWORK_CHECK_INTERVAL: int = 60
    NETWORK_TIMEOUT: int = 5

    # ===== 业务配置 =====

    # 操作超时设置
    USER_OPERATION_TIMEOUT: int = 60  # 用户操作超时时间（秒）
    ID_CARD_READ_TIMEOUT: int = 30  # 身份证读取超时
    FACE_RECOGNITION_TIMEOUT: int = 20  # 人脸识别超时
    QUERY_TIMEOUT: int = 45  # 查询超时
    PRINT_TIMEOUT: int = 120  # 打印超时

    # 重试配置
    MAX_RETRY_TIMES: int = 3
    RETRY_DELAY: int = 2  # 重试间隔（秒）

    # 数据保留配置
    USER_DATA_RETENTION_HOURS: int = 1  # 用户数据保留时间
    OPERATION_LOG_RETENTION_DAYS: int = 90  # 操作日志保留天数

    # ===== 开发调试配置 =====

    # 模拟设备（开发环境）
    MOCK_DEVICES: bool = False
    MOCK_GOVERNMENT_API: bool = False

    # 调试选项
    ENABLE_API_DOCS: bool = True
    ENABLE_CORS: bool = True
    CORS_ORIGINS: List[str] = ["*"]

    # 性能配置
    MAX_CONCURRENT_USERS: int = 5
    DATABASE_POOL_SIZE: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局设置实例
settings = Settings()


def get_settings() -> Settings:
    """获取设置实例"""
    return settings


# 环境检查函数
def check_environment():
    """检查运行环境"""
    errors = []

    # 检查必要目录
    required_dirs = [
        settings.TEMP_FILE_PATH,
        settings.OUTPUT_FILE_PATH,
        settings.LOG_FILE_PATH,
        settings.BACKUP_PATH,
    ]

    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            try:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"无法创建目录 {dir_path}: {e}")

    # 检查设备文件
    if settings.ID_CARD_READER_ENABLED:
        if not os.path.exists(settings.ID_CARD_READER_SDK_PATH):
            errors.append(
                f"身份证读卡器SDK文件不存在: {settings.ID_CARD_READER_SDK_PATH}"
            )

    # 检查串口设备
    device_ports = [
        settings.STAMP_DEVICE_PORT,
        settings.QR_SCANNER_PORT,
        settings.UPS_DEVICE_PORT,
        settings.LED_CONTROL_PORT,
    ]

    for port in device_ports:
        if port and not os.path.exists(port):
            errors.append(f"设备端口不存在: {port}")

    return errors


if __name__ == "__main__":
    # 环境检查
    errors = check_environment()
    if errors:
        print("❌ 环境检查失败:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ 环境检查通过")

    # 打印主要配置
    print(f"\n📋 当前配置:")
    print(f"应用名称: {settings.APP_NAME}")
    print(f"版本: {settings.APP_VERSION}")
    print(f"调试模式: {settings.DEBUG}")
    print(f"数据库: {settings.DATABASE_URL}")
    print(f"API前缀: {settings.API_V1_STR}")
