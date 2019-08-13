#!/bin/bash
# 发布脚本 ./relase.sh 0 0

# 脚本执行步骤
step=0
# 脚本执行每一步等待时间
waitSeconds=1
# 是否真实执行，*脚本第一个参数
if (( $1 ))
then
    isRealExcute=$1
else
    isRealExcute=0
fi
# 是否输入服务器ip，*脚本第二个参数
if (( $2 ))
then
    needInputRemoteIp=$2
else
    needInputRemoteIp=0
fi
needInputRemoteIp=0
# 默认服务器ip
remoteIp="xx.xx.xx.xx"
# 服务器密码
remotePasswd=""
# 项目名称配置
projects=(
"test01"
"test02"
"test03"
)

if (( ${needInputRemoteIp} == 1))
then
    let step+=1
    echo "${step}、请输入服务器ip"
    read remoteIp
fi

echo "要发布的服务器ip：${remoteIp}"
let step+=1
echo "${step}、请输入服务器密码"
read -s remotePasswd
sleep ${waitSeconds}s

let step+=1
echo "${step}、请选择您要发布项目?"
for i in "${!projects[@]}";
do
    echo "${i}) ${projects[${i}]}"
done
read projectNumber

projectName=${projects[${projectNumber}]}
echo "您将要发布的项目是：${projectName}"
sleep ${waitSeconds}s

# 本地项目路径
projectPath="/src/bak/git_tag/${projectName}"
# 线上项目备份路径
projectOnlineBakPath="/src/bak/online/${projectName}"
# 是否是新项目
isNewProject=0
if [ ! -e ${projectPath} ] 
then
    let step+=1
    isNewProject=1
    echo "${step}、项目不存在，尝试拉取代码"
    echo "git clone http://gitlab.xxx.com:81/vikey/${projectName}.git ${projectPath}"
    if (( ${isRealExcute} == 1))
    then
        git clone http://gitlab.xxx.com:81/vikey/${projectName}.git ${projectPath}
    fi
    sleep ${waitSeconds}s 
fi

let step+=1
echo "${step}、切换到项目目录"
echo "cd ${projectPath}"
if (( ${isRealExcute} == 1))
then
    cd ${projectPath}
fi
sleep ${waitSeconds}s

if (( ${isNewProject} == 0))
then
    if [ ! -e ${projectOnlineBakPath} ]
    then
        let step+=1
        echo "${step}、线上项目代码未存在，备份"
        echo "cp -r ${projectPath} /src/bak/online"
        if (( ${isRealExcute} == 1))
        then
            cp -r ${projectPath} /src/bak/online
        fi
    fi

    let step+=1
    echo "${step}、对项目代码执行更新"
    echo "git pull"
    if (( ${isRealExcute} == 1))
    then
        git pull
    fi
    sleep ${waitSeconds}s

    let step+=1
    echo "${step}、同步线上项目代码"
    echo "scp -r root@${remoteIp}:/src/${projectName} /src/bak/online"
    if (( ${isRealExcute} == 1))
    then
        sshpass -p ${remotePasswd} scp -r root@${remoteIp}:/src/${projectName} /src/bak/online
    fi
    sleep ${waitSeconds}s

    let step+=1
    echo "${step}、获取代码增量包"
    # 当前日期时间
    dateTime=$(date "+%Y%m%d%H%M%S")
    # 增量包名称
    increTar="${projectName}_${dateTime}.tar"
    # 增量包路径
    increTarPath="/src/bak"
    # 替换路径字符
    replaceStr="."
    echo "diff --brief -ruNa -X'/src/bak/git_tag/exclude.txt' ${projectPath} ${projectOnlineBakPath} | awk '{print\$2}' | sed 's#$projectPath#$replaceStr#g' | xargs tar -czvPf ${increTarPath}/${increTar}"
    if (( ${isRealExcute} == 1))
    then
        cd ${projectPath}
        diff --brief -ruNa -X'/src/bak/git_tag/exclude.txt' ${projectPath} ${projectOnlineBakPath} | awk '{print$2}' | sed "s#$projectPath#$replaceStr#g" | xargs tar -czvPf ${increTarPath}/${increTar}
    fi
    sleep ${waitSeconds}s

    let step+=1
    echo "${step}、同步增量包到线上"
    echo "scp ${increTarPath}/${increTar} root@${remoteIp}:/src/${projectName}"
    if (( ${isRealExcute} == 1))
    then
        sshpass -p ${remotePasswd} scp ${increTarPath}/${increTar} root@${remoteIp}:/src/${projectName}
    fi
    sleep ${waitSeconds}s

    # 增量包线上路径
    increTarOnlinePath="/src/${projectName}/${increTar}"
    echo "增量包的线上路径：${increTarOnlinePath}"

    let step+=1
    echo "${step}、线上服务器执行项目代码备份，并删除备份文件中的日志"
    # 线上项目备份路径
    bakPath="/src/backup/${projectName}_bak_${dateTime}"
    echo "ssh root@${remoteIp} 'cp -r /src/${projectName} ${bakPath} && rm -rf ${bakPath}/storage/logs'"
    if (( ${isRealExcute} == 1))
    then
        sshpass -p ${remotePasswd} ssh root@${remoteIp} "cp -r /src/${projectName} ${bakPath} && rm -rf ${bakPath}/storage/logs"
    fi
    sleep ${waitSeconds}s
else
    let step+=1
    echo "${step}、打包项目代码"
    # 当前日期时间
    dateTime=$(date "+%Y%m%d%H%M%S")
    # 增量包名称
    increTar="${projectName}_${dateTime}.tar"
    # 增量包路径
    increTarPath="/src/bak/${increTar}"
    echo "cd /src/bak/git_tag"
    echo "tar -czvPf ${increTarPath} ${projectName}"
    if (( ${isRealExcute} == 1))
    then
        cd /src/bak/git_tag
        tar -czvPf ${increTarPath} ${projectName}
    fi

    let step+=1
    echo "${step}、同步代码压缩包到线上"
    echo "scp ${increTarPath} root@${remoteIp}:/src"
    if (( ${isRealExcute} == 1))
    then
        sshpass -p ${remotePasswd} scp ${increTarPath} root@${remoteIp}:/src
    fi
    sleep ${waitSeconds}s

    # 增量包线上路径
    increTarOnlinePath="/src/${increTar}"
    echo "增量包的线上路径：${increTarOnlinePath}"
fi

let step+=1
echo "${step}、解压缩增量包"
echo "ssh root@${remoteIp} 'tar -xzvf ${increTarOnlinePath} -C /src/${projectName} && rm -f ${increTarOnlinePath}'"
if (( ${isRealExcute} == 1))
then
    sshpass -p ${remotePasswd} ssh root@${remoteIp} "tar -xzvf ${increTarOnlinePath} -C /src/${projectName} && rm -f ${increTarOnlinePath}"
fi

echo "恭喜，发布完成~"
echo -e "\n"
echo -e "\e[1;41mtips: 如需回滚，请在服务器（${remoteIp}）执行如下命令 \e[0m"
echo -e "\e[1;41m      cp -r ${bakPath} /src/${projectName} \e[0m"

