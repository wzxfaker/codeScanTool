#!/bin/bash

echo $1
echo $2
echo $3
source_path=$1
archive_path=$2
build_type=$3

output_dir="${source_path}/scan" 
macho_dir="${archive_path}/Products/Applications/Waha.app"

echo "macho_dir = ${macho_dir}"
rm -rf $output_dir
mkdir $output_dir
# cd "${output_dir}/Products/Applications/Waha"

strings - -a -arch arm64 "${macho_dir}/Waha" | grep -i pay | grep -i chat > "${output_dir}/chatpay.txt"
strings - -a -arch arm64 "${macho_dir}/Waha" | grep -i pay > "${output_dir}/pay.txt"
strings - -a -arch arm64 "${macho_dir}/Waha" | grep -i charge > "${output_dir}/charge.txt"
# video过滤扫描
strings - -a -arch arm64 "${macho_dir}/Waha" | grep -i video | grep -v AV > "${output_dir}/video.txt"
# per过滤扫描
strings - -a -arch arm64 "${macho_dir}/Waha" | grep -i per \
                                             | grep -i -v helper \
                                             | grep -i -v typer \
                                             | grep -i -v super \
                                             | grep -i -v Developer \
                                             | grep -i -v Proper \
                                             | grep -i -v Apper \
                                             | grep -i -v oper \
                                             | grep -i -v Cropper \
                                             | grep -i -v Keeper \
                                             | grep -i -v Upper \
                                             | grep -i -v adaper \
                                             | grep [pP][eE][rR][_A-Z] \
                                             > "${output_dir}/per.txt"
# message过滤扫描
message=$(strings - -a -arch arm64 "${macho_dir}/Waha" | grep -i message)
echo "${message}" | grep -i lottery >> "${output_dir}/message.txt"
echo "${message}" | grep -i diamond >> "${output_dir}/message.txt"
echo "${message}" | grep -i game >> "${output_dir}/message.txt"
echo "${message}" | grep -i free >> "${output_dir}/message.txt"
echo "${message}" | grep -i repacket >> "${output_dir}/message.txt"
echo "${message}" | grep -i price >> "${output_dir}/message.txt"
echo "${message}" | grep -i pay >> "${output_dir}/message.txt"
echo "${message}" | grep -i earn >> "${output_dir}/message.txt"
echo "${message}" | grep -i paid >> "${output_dir}/message.txt"

echo "------关键字扫描------\n" >> "${output_dir}/count.txt"
count=$(wc -l "${output_dir}/chatpay.txt")
echo "1.chat&pay ${count} \n" >> "${output_dir}/count.txt"
count=$(wc -l "${output_dir}/pay.txt")
echo "2.pay ${count} \n" >> "${output_dir}/count.txt"
count=$(wc -l "${output_dir}/charge.txt")
echo "3.charge ${count} \n" >> "${output_dir}/count.txt"
count=$(wc -l "${output_dir}/video.txt")
echo "4.video ${count} \n" >> "${output_dir}/count.txt"
count=$(wc -l "${output_dir}/per.txt")
echo "5.per ${count} \n" >> "${output_dir}/count.txt"
count=$(wc -l "${output_dir}/message.txt")
echo "6.message ${count} \n" >> "${output_dir}/count.txt"

index=7
list=("chatrecharge" "switch" "hidden" "alpha" "opaque" "hide" "coin" "game" "earn" "reward" "free" "price" "paid" "cost" "diamonds" "articles")
for name in ${list[@]} 
do
    # echo $name
    # echo $index
    strings - -a -arch arm64 "${macho_dir}/Waha" | grep -i ${name} > "${output_dir}/${name}.txt"
    count=$(wc -l "${output_dir}/${name}.txt")
    echo "$index.$name ${count} \n" >> "${output_dir}/count.txt"

    let index++
done;

echo "------start tar------\n"
files_tar_dir="${source_path}/scan_files.tar.gz"
echo "------start tar path ${files_tar_dir} ------\n"
tar zcvf $files_tar_dir $output_dir
echo "------start end------\n"
