import arcpy
import pandas as pd


def build_df_from_arcpy(table, index_col=None): #insert shp-path
    """
    Build a pandas dataframe from an ArcGIS Feature Class.

    Uses the arcpy Search Cursor to loop over a feature class in pandas and
    generate a pandas dataframe. If the dataset is a feature class with a
    geometry it will calculate the length and the area before returning, and
    the geometry will be returned as well-known-text.

    :param table: The path to the feature class or table
    :type table: str
    :param index_col: A column to use as the dataframe index. If not supplied
                      for feature classes use the Object ID
    :type index_col: str
    :return: dataframe representation of the feature class. Note this is all in
             memory, so be careful with really big datasets!
    :rtype: pd.DataFrame
    """

    desc = arcpy.Describe(table)
    cursor = arcpy.SearchCursor(table)

    new_data = []

    for row in cursor:
        new_row = {}
        for field in desc.fields:
            new_row[field.aliasName or field.name] = row.getValue(field.name)
        new_data.append(new_row)

    try:
        if not index_col:
            index_col = desc.OIDFieldName

        df = pd.DataFrame(new_data).set_index(index_col)
        df["SHAPEArea"] = df[desc.shapeFieldName].apply(lambda g: g.area)
        df["SHAPELength"] = df[desc.shapeFieldName].apply(lambda g: g.length)
        df[desc.shapeFieldName] = df[desc.shapeFieldName].apply(lambda g: g.WKT)
    except AttributeError:
        # If this is a table in the datbase or on disk, in ArcGIS it won't have
        # either an OID field, nor a geometry
        pass

    return df