/***************************************************************************
 *   Copyright (c) 2015 WandererFan <wandererfan@gmail.com>                *
 *                                                                         *
 *   This file is part of the FreeCAD CAx development system.              *
 *                                                                         *
 *   This library is free software; you can redistribute it and/or         *
 *   modify it under the terms of the GNU Library General Public           *
 *   License as published by the Free Software Foundation; either          *
 *   version 2 of the License, or (at your option) any later version.      *
 *                                                                         *
 *   This library  is distributed in the hope that it will be useful,      *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU Library General Public License for more details.                  *
 *                                                                         *
 *   You should have received a copy of the GNU Library General Public     *
 *   License along with this library; see the file COPYING.LIB. If not,    *
 *   write to the Free Software Foundation, Inc., 59 Temple Place,         *
 *   Suite 330, Boston, MA  02111-1307, USA                                *
 *                                                                         *
 ***************************************************************************/

#ifndef _Drawing_DrawHatch_h_
#define _Drawing_DrawHatch_h_

# include <App/DocumentObject.h>
# include <App/FeaturePython.h>
# include <App/PropertyLinks.h>
#include <App/PropertyFile.h>

#include "DrawView.h"
#include "DrawViewPart.h"

namespace TechDraw
{

class DrawingExport DrawHatch : public TechDraw::DrawView
{
    PROPERTY_HEADER(TechDraw::DrawHatch);

public:
    DrawHatch();
    virtual ~DrawHatch();

    App::PropertyLink        PartView;
    App::PropertyVector      DirProjection;                            //edge list is only valid for original projection?
    App::PropertyLinkSubList Edges;
    App::PropertyFile        HatchPattern;
    App::PropertyColor       HatchColor;

    //short mustExecute() const;

    virtual App::DocumentObjectExecReturn *execute(void);

    virtual const char* getViewProviderName(void) const {
        return "TechDrawGui::ViewProviderHatch";
    }

    //DrawViewPart* getViewPart() const;

protected:
    void onChanged(const App::Property* prop);

private:
};

typedef App::FeaturePythonT<DrawHatch> DrawHatchPython;

} //namespace TechDraw
#endif