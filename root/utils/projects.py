def create_basic_folders(base_dir, media_root):
    import os
    logs_root_path = os.path.join(base_dir, 'logs')
    static_root_path = os.path.join(base_dir, 'static')
    static_root_path2 = os.path.join(base_dir, 'root', 'static')

    FOLDERS = [logs_root_path, static_root_path, static_root_path2, media_root]
    for f in FOLDERS:
        if not os.path.isdir(f):
            os.mkdir(f)
