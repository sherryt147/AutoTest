*** Settings ***
Documentation     测试芯片的射频相关性能。
Library           BuiltIn
Library           ../../Driver/NPSC2038/NPSC2038Driver.py
Library           ../../Driver/NPSC2038/NPSC2038TestCase.py
Library           ../../Driver/Instrument/AgilentN9020A.py

*** Variables ***
${FREQ}           223
${RF_LOSS}        0.5

*** Test Cases ***
发射功率Min
    [Documentation]    说明：测试发射功率最小值
    ...    指标：-40dBm±1dBm
    [Tags]    TX    发射功率    ${FREQ}MHz
    set_freq_tx    ${FREQ}
    set_power    MIN
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    -20
    ${POWER}    getChannelPower
    Should Be True    -39>${POWER} > -41
    Log    The result is ${POWER}    # 在日志文件中记录结果信息
    Set Test Message    ${POWER}dBm    # 将测试结果显示在测试报告的message表格中

发射功率步进
    [Documentation]    说明：射频发射功率调整步进（-40dBm~-20dBm）
    ...    指标：3dB±1
    [Tags]    TX    发射功率    ${FREQ}MHz
    ${Result}    TestPowerStep_Minus20dBm    ${RF_LOSS}
    Should Be True    0<${Result} < 4
    Log    The result is ${Result}    # 在日志文件中记录结果信息
    Set Test Message    ${Result}dBm    # 将测试结果显示在测试报告的message表格中

发射功率步进2
    [Documentation]    说明：射频发射功率调整步进（-20dBm~20dBm）
    ...    指标：1dB
    [Tags]    TX    发射功率    ${FREQ}MHz
    ${Result}    TestPowerStep_20dBm    ${RF_LOSS}
    Should Be True    0<${Result} < 4
    Log    The result is ${Result}    # 在日志文件中记录结果信息
    Set Test Message    ${Result}dBm    # 将测试结果显示在测试报告的message表格中

发射功率Max
    [Documentation]    说明：射频发射最大发射功率
    ...    指标：20dBm±1dBm
    [Tags]    TX    发射功率    ${FREQ}MHz
    [Timeout]    30 seconds
    set_freq_tx    ${FREQ}
    set_power    MAX
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setSpanMHz    20
    setReferenceLevelDBM    20
    ${POWER}    getChannelPower
    Should Be True    21>${POWER} > 19
    Log    The result is ${POWER}    # 在日志文件中记录结果信息
    Set Test Message    ${POWER}dBm    # 将测试结果显示在测试报告的message表格中

二次谐波
    [Documentation]    说明：测量信号的二次谐波功率
    ...    指标：<-45dBc
    [Tags]    TX    ${FREQ}MHz
    set_freq_tx    ${FREQ}
    set_power    MAX
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${POWER}    getHarmonic2nd    ${FREQ}
    Should Be True    ${POWER} <-45
    Log    The result is ${POWER}    # 在日志文件中记录结果信息
    Set Test Message    ${POWER}dBc    # 将测试结果显示在测试报告的message表格中

三次谐波
    [Documentation]    说明：测量信号的三次谐波功率
    ...    指标：-55dBc
    [Tags]    TX    ${FREQ}MHz
    set_freq_tx    ${FREQ}
    start_tramsmit
    set_power    MAX
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${POWER}    getHarmonic3nd    ${FREQ}
    Should Be True    ${POWER} <-55
    Log    The result is ${POWER}    # 在日志文件中记录结果信息
    Set Test Message    ${POWER}dBc    # 将测试结果显示在测试报告的message表格中

邻道泄露功率比
    [Documentation]    说明：测量ACP值
    ...    指标：<-40dBc
    [Tags]    TX    ${FREQ}MHz
    setCentralFreqMHz    ${FREQ}
    ${ACP}    getACP
    Should Be True    ${ACP}<-40
    Log    The result is ${ACP}    # 在日志文件中记录结果信息
    Set Test Message    ${ACP}dBc    # 将测试结果显示在测试报告的message表格中

次邻道泄露功率比
    [Documentation]    说明：测量ACP值
    ...    指标：-50dBc
    [Tags]    TX    ${FREQ}MHz
    setCentralFreqMHz    ${FREQ}
    ${ACP}    getACP
    Should Be True    ${ACP}<-40
    Log    The result is ${ACP}    # 在日志文件中记录结果信息
    Set Test Message    ${ACP}dBc    # 将测试结果显示在测试报告的message表格中

PA关断功率
    [Documentation]    说明：测试芯片PA关断情况下输出功率
    ...    指标：≤85dBm
    [Tags]    TX

杂散辐射1
    [Documentation]    说明：测试杂散辐射（9kHz~150KHz）
    ...    指标：<-40dBm
    [Tags]    TX    ${FREQ}MHz
    set_freq_tx    ${FREQ}
    set_power    MAX
    start_tramsmit
    ${Result}    getSpurEm    1KHz    -40    9KHz    150KHz
    Should Be True    ${Result} >0
    Log    The result is ${Result}    # 在日志文件中记录结果信息
    Set Test Message    ${Result}    # 将测试结果显示在测试报告的message表格中

杂散辐射2
    [Documentation]    说明：测试杂散辐射（150kHz~30MHz）
    ...    指标：<-40dBm
    [Tags]    TX    ${FREQ}MHz
    set_freq_tx    ${FREQ}
    set_power    MAX
    start_tramsmit
    ${Result}    getSpurEm    10KHz    -40    150KHz    30MHz
    Should Be True    ${Result} >0
    Log    The result is ${Result}    # 在日志文件中记录结果信息
    Set Test Message    ${Result}    # 将测试结果显示在测试报告的message表格中

杂散辐射3
    [Documentation]    说明：测试杂散辐射（30MHz~1GHz）
    ...    指标：<-40dBm
    [Tags]    TX    ${FREQ}MHz
    set_freq_tx    ${FREQ}
    set_power    MAX
    start_tramsmit
    ${Result}    getSpurEm    100KHz    -40    30MHz    1GHz
    Should Be True    ${Result} >0
    Log    The result is ${Result}    # 在日志文件中记录结果信息
    Set Test Message    ${Result}    # 将测试结果显示在测试报告的message表格中

杂散辐射4
    [Documentation]    说明：测试杂散辐射（1GHz~12.75GHz）
    ...    指标：<-35dBm
    [Tags]    TX    ${FREQ}MHz
    set_freq_tx    ${FREQ}
    set_power    MAX
    start_tramsmit
    ${Result}    getSpurEm    1MHz    -35    1GHz    12.75GHz
    Should Be True    ${Result} >0
    Log    The result is ${Result}    # 在日志文件中记录结果信息
    Set Test Message    ${Result}    # 将测试结果显示在测试报告的message表格中

带外辐射
    [Documentation]    说明：测试带外辐射（±100KHz）
    ...    指标：<-15dBm
    [Tags]    TX    ${FREQ}MHz
    set_freq_tx    ${FREQ}
    set_power    MAX
    start_tramsmit
    ${ResH}    Evaluate    ${FREQ}+0.1
    ${ResL}    Evaluate    ${FREQ}-0.1
    ${Result}    getSpurEm    50KHz    -15    ${ResL}MHz    ${ResH}MHz
    Should Be True    ${Result} < -15
    Log    The result is ${Result}    # 在日志文件中记录结果信息
    Set Test Message    ${Result}dBm    # 将测试结果显示在测试报告的message表格中

发射互调
    [Tags]    TX    ${FREQ}MHz
