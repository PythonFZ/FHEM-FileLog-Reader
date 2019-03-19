import pandas as pd

def filelog_reader(file_list):
    '''

    Parameters
    ----------
    file_list: list
        List of all FHEM FileLog-Files that should be processed!

    Returns
    -------
    my_df: pd.DataFrame
        sorted DataFrame in the style of dblog

    Notes
    ------
    There can be errors with FileLogs that do not match the TimeStamp or do have Readings with blanks or the
    state reading contains blanks!

    '''
    my_df = pd.DataFrame(None)
    for path in file_list:
        my_data = []
        f = open(path, "r")
        for line in f:
            line = line.split()
            # Funktioniert, außer wenn state ein Leerzeichen hat!
            if len(line) == 3:
                line = [line[0], line[1], 'state', line[2]]
            if len(line) > 4:
                line = [line[0], line[1], line[2], " ".join(line[3:])]
            my_data.append(line)
        df = pd.DataFrame(my_data, columns=['timestamp', 'device', 'reading', 'state'])
        df = df.set_index('timestamp')
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d_%H:%M:%S')
        my_df = pd.concat([my_df, df])
    my_df.sort_index(inplace=True)

    return my_df

if __name__ == '__main__':
    my_files = ['./FileLog/Badezimmer.Heizung-2018.log', './FileLog/Badezimmer.Thermostat-2018.log',
                './FileLog/BriefkastenSensor-2018.log']

    this_df = filelog_reader(my_files)
    print(this_df)