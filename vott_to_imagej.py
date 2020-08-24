import os
import json


# calculate 4 points
def hwlt_to_4points(height, width, left, top):
    x1 = left
    y1 = top
    x2 = left + width
    y2 = top
    x3 = left + width
    y3 = top + height
    x4 = left
    y4 = top + height
    return [x1, y1, x2, y2, x3, y3, x4, y4]


def get_bbox_info(json_path):
    # read json file
    with open(json_path) as f:
        data = json.load(f)
        # get the bounding box information
        bbox_list = []
        # get file name
        asset = data['asset']
        image_name_jpg = asset['name']
        # remove jpg extension
        image_name = os.path.splitext(image_name_jpg)[0]
        # iterate through the information
        for item in data.get('regions'):
            height = item.get('boundingBox').get('height')
            width = item.get('boundingBox').get('width')
            left = item.get('boundingBox').get('left')
            top = item.get('boundingBox').get('top')
            four_points = hwlt_to_4points(height, width, left, top)
            tag = item.get('tags')[0]
            # tag string->lowercase
            tag = tag.lower()
            # remove spaces in tag
            tag = tag.strip()
            # put tags at the beginning of the four_points list
            four_points_str = [str(x) for x in four_points]
            four_points_str.insert(0, tag)

            bbox_list.append(four_points_str)
    return image_name, bbox_list


def main():
    root_path = '/home/sarah/projects/ui_data_v12/ui/train_vott'

    # output txt file will be saved here
    output_path = '/home/sarah/projects/ui_data_v12/ui/train'

    for vott_file_name in os.listdir(root_path):
        if vott_file_name.endswith('.json'):
            image_name, bbox_list = get_bbox_info(os.path.join(root_path, vott_file_name))
            # create a text file with image name and .txt extension
            image_txt = image_name + '.txt'
            txt_file = os.path.join(output_path, image_txt)
            # separate each list element in a bounding box with tabs \t
            with open(txt_file, 'a') as output:
                for element in bbox_list:
                    line = '\t'.join(element)
            # separate each bounding box with new line \n
                    output.write(line + '\n')


if __name__ == '__main__':
    main()
