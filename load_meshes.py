import os
import bpy


def read_buffer(filepath):
    with open(filepath, 'r') as file:
        txt_buffer = file.readlines()

    txt_buffer = txt_buffer[3:].copy()

    coords = [(float(txt_buffer[i].strip().split(' ')[-4:-1][0][1:-1]),
               float(txt_buffer[i].strip().split(' ')[-4:-1][2][:-1]),
               float(txt_buffer[i].strip().split(' ')[-4:-1][1][:-1]))
              for i in range(len(txt_buffer))]

    angles = [float(txt_buffer[i].strip().split(' ')[-1])
              for i in range(len(txt_buffer))]

    ids = [int(txt_buffer[i].strip().split(' ')[1])
           for i in range(len(txt_buffer))]

    non_zeroed = ([], [], [])
    assert len(coords) == len(angles) == len(ids)
    for i in range(len(ids)):
        if coords[i] != (0.0, 0.0, 0.0):
            non_zeroed[0].append(coords[i])
            non_zeroed[1].append(angles[i])
            non_zeroed[2].append(ids[i])

    return non_zeroed


def read_buffer_dims(filepath):
    with open(filepath, 'r') as file:
        txt_buffer = file.readlines()

    txt_buffer = txt_buffer[3:].copy()

    coords = [(float(txt_buffer[i].strip().split(' ')[-7:-4][0][1:-1]),
               float(txt_buffer[i].strip().split(' ')[-7:-4][2][:-1]),
               float(txt_buffer[i].strip().split(' ')[-7:-4][1][:-1]))
              for i in range(len(txt_buffer))]

    angles = [float(txt_buffer[i].strip().split(' ')[-4])
              for i in range(len(txt_buffer))]

    ids = [int(txt_buffer[i].strip().split(' ')[1])
           for i in range(len(txt_buffer))]

    dims = [(float(txt_buffer[i].strip().split(' ')[-3:][0][1:-1]),
             float(txt_buffer[i].strip().split(' ')[-3:][2][:-1]),
             float(txt_buffer[i].strip().split(' ')[-3:][1][:-1]))
            for i in range(len(txt_buffer))]

    non_zeroed = ([], [], [], [])
    assert len(coords) == len(angles) == len(ids) == len(dims)
    for i in range(len(ids)):
        if coords[i] != (0.0, 0.0, 0.0):
            non_zeroed[0].append(coords[i])
            non_zeroed[1].append(angles[i])
            non_zeroed[2].append(ids[i])
            non_zeroed[3].append(dims[i])
    return non_zeroed


def find_lowest_z(filepath):
    coords, _, _ = read_buffer(filepath=filepath)
    sorted_coords = sorted(coords, key=lambda x: x[2], reverse=False)
    return sorted_coords[0][2]


def create_scene_dims(meshpath, ids, coords, angles, dims):
    if (not os.path.exists(meshpath.split('\\')[-2])):
        os.mkdir(meshpath.split('\\')[-2])
    savepath = meshpath.split('\\')[-2]
    scene = bpy.context.scene
    i = 0
    for _id, coord, angle, dim in zip(ids, coords, angles, dims):
        try:
            print(_id)
            bpy.ops.import_scene.obj(filepath=meshpath + '/' +
                                     str(_id) + '.obj')
            scene.objects[i+3].location = coord
            scene.objects[i+3].rotation_euler[2] = -angle
            scene.objects[i+3].dimensions = dim

            if i % 1000 == 0 and i != 0:
                bpy.ops.wm.save_as_mainfile(filepath=savepath + '/scene'
                                            + str(i) + '.blend')
            i += 1
        except RuntimeError:
            pass

    bpy.ops.wm.save_as_mainfile(filepath=savepath +
                                '/scene_final_notzeroed.blend')


def create_scene(meshpath, ids, coords, angles):
    if (not os.path.exists(meshpath.split('\\')[-2])):
        os.mkdir(meshpath.split('\\')[-2])
    savepath = meshpath.split('\\')[-2]
    scene = bpy.context.scene
    i = 0
    for _id, coord, angle in zip(ids, coords, angles):
        try:
            print(_id)
            bpy.ops.import_scene.obj(filepath=meshpath + '/' +
                                     str(_id) + '.obj')
            scene.objects[i+3].location = coord
            scene.objects[i+3].rotation_euler[2] = -angle

            if i % 1000 == 0 and i != 0:
                bpy.ops.wm.save_as_mainfile(filepath=savepath + '/scene'
                                            + str(i) + '.blend')
            i += 1
        except RuntimeError:
            pass

    bpy.ops.wm.save_as_mainfile(filepath=savepath +
                                '/scene_final_notzeroed.blend')


def main():
    WORKING_DIRECTORY = "./"
    cities = ['mega_city']
    check = sum(map(lambda x: os.path.exists(x), cities))
    assert check == len(cities)
    for city in cities:
        path_txt = os.path.join(WORKING_DIRECTORY, city,
                                'building_pos_angle.txt')
        coords, angles, ids, dims = read_buffer_dims(path_txt)
        path_meshes = os.path.join(WORKING_DIRECTORY, city, 'meshes')
        create_scene_dims(path_meshes, ids, coords, angles, dims)


if __name__ == '__main__':

    main()
    # cities = ['new_europe', 'dallas', 'islo3', 'LGR', 'mega_city', 'Ralf1']
    # for city in cities:
    #     print(f"Lowest building of {city} is on " +
    #           f"{find_lowest_z(f'./{city}/building_pos_angle.txt')}")
