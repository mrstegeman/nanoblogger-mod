#!/bin/bash

BLOG_DIR=`dirname $(pwd)`
. "$BLOG_DIR/blog.conf"
DATE_CMD="date"
POST_DATA=$(</dev/stdin)
IDS=`echo "$QUERY_STRING" | grep -oE "(^|[?&])id=[^&]+" | cut -f 2 -d "=" | head -n1`
ACTION=`echo "$QUERY_STRING" | grep -oE "(^|[?&])action=[^&]+" | cut -f 2 -d "="`

case "$ACTION" in
    count)
        echo "Status: 200 OK"
        echo
        echo "{"
        idlist=(`echo "$IDS" | tr -s ',' ' '`)
        for id in "${idlist[@]}"
        do
            ID=`echo "$id" | sed -e 's/^e//' -e 's/\.txt$//'`
            count=`ls -1 "$BLOG_DIR/comments/$ID" | wc -l`
            echo "\"e$ID.txt\": $count,"
        done
        echo "}"
        ;;
    get)
        echo "Status: 200 OK"
        echo
        echo "{\"comments\": ["
        idlist=(`echo "$IDS" | tr -s ',' ' '`)
        for id in "${idlist[@]}"
        do
            ID=`echo "$id" | sed -e 's/^e//' -e 's/\.txt$//'`
            for file in `find $BLOG_DIR/comments/$ID/ -name '*.txt' | sort`
            do
                date=`grep -E 'DATE::' "$file" | sed 's/^DATE:://' | head -n1`
                title=`grep -E 'TITLE::' "$file" | sed 's/^TITLE:://' | head -n1`
                author=`grep -E 'AUTHOR::' "$file" | sed 's/^AUTHOR:://' | head -n1`
                body=`grep -E 'BODY::' "$file" | sed 's/^BODY:://' | head -n1`
                echo "{\"title\": \"$title\","
                echo "\"date\": \"$date\","
                echo "\"author\": \"$author\","
                echo "\"body\": \"$body\"},"
            done
        done
        echo "]}"
        ;;
    put)
        plist=(`echo "$POST_DATA" | tr -s '&' ' '`)
        page=""
        idlist=(`echo "$IDS" | tr -s ',' ' '`)
        ID=`echo "${idlist[0]}" | sed -e 's/^e//' -e 's/\.txt$//'`
        if [ ! -d "$BLOG_DIR/comments/$ID" ]; then
            mkdir "$BLOG_DIR/comments/$ID"
            if [ $? -ne 0 ]; then
                echo "Status: 500 Internal Server Error"
                echo
                exit 1
            fi
        fi
        pnum=`ls -1 -r "$BLOG_DIR/comments/$ID" | head -n 1 | sed 's/\.txt$//'`
        pnum=$(($pnum+1))
        file="$BLOG_DIR/comments/$ID/$pnum.txt"
        if [ -n "$DATE_FORMAT" ]; then
            if [ -n "$DATE_LOCALE" ]; then
                curdate=`LC_ALL="$DATE_LOCALE" $DATE_CMD +"$DATE_FORMAT" $DATE_ARGS`
            else
                curdate=`$DATE_CMD +"$DATE_FORMAT" $DATE_ARGS`
            fi
        else
            if [ -n "$DATE_LOCALE" ]; then
                curdate=`LC_ALL="$DATE_LOCALE" $DATE_CMD $DATE_ARGS`
            else
                curdate=`$DATE_CMD $DATE_ARGS`
            fi
        fi
        echo "DATE::$curdate" > "$file"
        for param in "${plist[@]}"
        do
            name=`echo "$param" | cut -d '=' -f 1`
            val=`echo "$param" | cut -d '=' -f 2-`
            case "$name" in
                title)
                    echo "TITLE::$val" >> "$file"
                    ;;
                name)
                    echo "AUTHOR::$val" >> "$file"
                    ;;
                comment)
                    echo "BODY::$val" >> "$file"
                    ;;
                page)
                    page=$(echo -n "$val" | sed 's/\\/\\\\/g;s/\(%\)\([0-9a-fA-F][0-9a-fA-F]\)/\\x\2/g')
                    page=`printf "$page"`
                    ;;
            esac
        done
        echo "Location: $page"
        echo
        ;;
esac
