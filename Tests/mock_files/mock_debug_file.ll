; ModuleID = '<stdin>'
source_filename = "struct_example.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

%struct.Person = type { [50 x i8], i32 }
%struct.Test = type { i32 }

@global = dso_local global i32 0, align 4, !dbg !0
@.str = private unnamed_addr constant [10 x i8] c"Name: %s\0A\00", align 1, !dbg !22
@.str.1 = private unnamed_addr constant [9 x i8] c"Age: %d\0A\00", align 1, !dbg !27
@.str.2 = private unnamed_addr constant [26 x i8] c"Memory allocation failed\0A\00", align 1, !dbg !32
@.str.3 = private unnamed_addr constant [6 x i8] c"Alice\00", align 1, !dbg !37
@.str.4 = private unnamed_addr constant [16 x i8] c"Test value: %d\0A\00", align 1, !dbg !42
@.str.5 = private unnamed_addr constant [21 x i8] c"Global Variable: %d\0A\00", align 1, !dbg !47

; Function Attrs: noinline nounwind uwtable
define dso_local void @print_person(ptr noundef %0) #0 !dbg !60 {
  tail call void @llvm.dbg.value(metadata ptr %0, metadata !66, metadata !DIExpression()), !dbg !67
  %2 = getelementptr inbounds %struct.Person, ptr %0, i32 0, i32 0, !dbg !68
  %3 = getelementptr inbounds [50 x i8], ptr %2, i64 0, i64 0, !dbg !69
  %4 = call i32 (ptr, ...) @printf(ptr noundef @.str, ptr noundef %3), !dbg !70
  %5 = getelementptr inbounds %struct.Person, ptr %0, i32 0, i32 1, !dbg !71
  %6 = load i32, ptr %5, align 4, !dbg !71
  %7 = call i32 (ptr, ...) @printf(ptr noundef @.str.1, i32 noundef %6), !dbg !72
  ret void, !dbg !73
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

declare i32 @printf(ptr noundef, ...) #2

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 !dbg !74 {
  %1 = call noalias ptr @malloc(i64 noundef 56) #5, !dbg !77
  tail call void @llvm.dbg.value(metadata ptr %1, metadata !78, metadata !DIExpression()), !dbg !79
  %2 = call noalias ptr @malloc(i64 noundef 4) #5, !dbg !80
  tail call void @llvm.dbg.value(metadata ptr %2, metadata !81, metadata !DIExpression()), !dbg !79
  %3 = icmp eq ptr %1, null, !dbg !82
  br i1 %3, label %4, label %6, !dbg !84

4:                                                ; preds = %0
  %5 = call i32 (ptr, ...) @printf(ptr noundef @.str.2), !dbg !85
  br label %21, !dbg !87

6:                                                ; preds = %0
  %7 = icmp eq ptr %2, null, !dbg !88
  br i1 %7, label %8, label %10, !dbg !90

8:                                                ; preds = %6
  %9 = call i32 (ptr, ...) @printf(ptr noundef @.str.2), !dbg !91
  br label %21, !dbg !93

10:                                               ; preds = %6
  %11 = getelementptr inbounds %struct.Person, ptr %1, i32 0, i32 0, !dbg !94
  %12 = getelementptr inbounds [50 x i8], ptr %11, i64 0, i64 0, !dbg !95
  %13 = call ptr @strcpy(ptr noundef %12, ptr noundef @.str.3) #6, !dbg !96
  %14 = getelementptr inbounds %struct.Person, ptr %1, i32 0, i32 1, !dbg !97
  store i32 25, ptr %14, align 4, !dbg !98
  %15 = getelementptr inbounds %struct.Test, ptr %2, i32 0, i32 0, !dbg !99
  store i32 80, ptr %15, align 4, !dbg !100
  call void @print_person(ptr noundef %1), !dbg !101
  %16 = getelementptr inbounds %struct.Test, ptr %2, i32 0, i32 0, !dbg !102
  %17 = load i32, ptr %16, align 4, !dbg !102
  %18 = call i32 (ptr, ...) @printf(ptr noundef @.str.4, i32 noundef %17), !dbg !103
  %19 = load i32, ptr @global, align 4, !dbg !104
  %20 = call i32 (ptr, ...) @printf(ptr noundef @.str.5, i32 noundef %19), !dbg !105
  call void @free(ptr noundef %1) #6, !dbg !106
  call void @free(ptr noundef %2) #6, !dbg !107
  br label %21, !dbg !108

21:                                               ; preds = %10, %8, %4
  %.0 = phi i32 [ 1, %4 ], [ 1, %8 ], [ 0, %10 ], !dbg !79
  ret i32 %.0, !dbg !109
}

; Function Attrs: nounwind allocsize(0)
declare noalias ptr @malloc(i64 noundef) #3

; Function Attrs: nounwind
declare ptr @strcpy(ptr noundef, ptr noundef) #4

; Function Attrs: nounwind
declare void @free(ptr noundef) #4

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare void @llvm.dbg.value(metadata, metadata, metadata) #1

attributes #0 = { noinline nounwind uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #2 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { nounwind allocsize(0) "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { nounwind "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #5 = { nounwind allocsize(0) }
attributes #6 = { nounwind }

!llvm.dbg.cu = !{!2}
!llvm.module.flags = !{!52, !53, !54, !55, !56, !57, !58}
!llvm.ident = !{!59}

!0 = !DIGlobalVariableExpression(var: !1, expr: !DIExpression())
!1 = distinct !DIGlobalVariable(name: "global", scope: !2, file: !3, line: 5, type: !15, isLocal: false, isDefinition: true)
!2 = distinct !DICompileUnit(language: DW_LANG_C11, file: !3, producer: "Ubuntu clang version 18.1.8 (++20240731025043+3b5b5c1ec4a3-1~exp1~20240731145144.92)", isOptimized: false, flags: "/usr/lib/llvm-18/bin/clang -S -g -O0 -emit-llvm struct_example.c -o -", runtimeVersion: 0, emissionKind: FullDebug, retainedTypes: !4, globals: !21, splitDebugInlining: false, nameTableKind: None)
!3 = !DIFile(filename: "struct_example.c", directory: "/home/eclypsium/Desktop", checksumkind: CSK_MD5, checksum: "32c55280e642a885f00ea909b5391003")
!4 = !{!5, !16, !20}
!5 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !6, size: 64)
!6 = !DIDerivedType(tag: DW_TAG_typedef, name: "Person", file: !3, line: 11, baseType: !7)
!7 = distinct !DICompositeType(tag: DW_TAG_structure_type, file: !3, line: 8, size: 448, elements: !8)
!8 = !{!9, !14}
!9 = !DIDerivedType(tag: DW_TAG_member, name: "name", scope: !7, file: !3, line: 9, baseType: !10, size: 400)
!10 = !DICompositeType(tag: DW_TAG_array_type, baseType: !11, size: 400, elements: !12)
!11 = !DIBasicType(name: "char", size: 8, encoding: DW_ATE_signed_char)
!12 = !{!13}
!13 = !DISubrange(count: 50)
!14 = !DIDerivedType(tag: DW_TAG_member, name: "age", scope: !7, file: !3, line: 10, baseType: !15, size: 32, offset: 416)
!15 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!16 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !17, size: 64)
!17 = distinct !DICompositeType(tag: DW_TAG_structure_type, name: "Test", file: !3, line: 13, size: 32, elements: !18)
!18 = !{!19}
!19 = !DIDerivedType(tag: DW_TAG_member, name: "field", scope: !17, file: !3, line: 14, baseType: !15, size: 32)
!20 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: null, size: 64)
!21 = !{!0, !22, !27, !32, !37, !42, !47}
!22 = !DIGlobalVariableExpression(var: !23, expr: !DIExpression())
!23 = distinct !DIGlobalVariable(scope: null, file: !3, line: 18, type: !24, isLocal: true, isDefinition: true)
!24 = !DICompositeType(tag: DW_TAG_array_type, baseType: !11, size: 80, elements: !25)
!25 = !{!26}
!26 = !DISubrange(count: 10)
!27 = !DIGlobalVariableExpression(var: !28, expr: !DIExpression())
!28 = distinct !DIGlobalVariable(scope: null, file: !3, line: 19, type: !29, isLocal: true, isDefinition: true)
!29 = !DICompositeType(tag: DW_TAG_array_type, baseType: !11, size: 72, elements: !30)
!30 = !{!31}
!31 = !DISubrange(count: 9)
!32 = !DIGlobalVariableExpression(var: !33, expr: !DIExpression())
!33 = distinct !DIGlobalVariable(scope: null, file: !3, line: 28, type: !34, isLocal: true, isDefinition: true)
!34 = !DICompositeType(tag: DW_TAG_array_type, baseType: !11, size: 208, elements: !35)
!35 = !{!36}
!36 = !DISubrange(count: 26)
!37 = !DIGlobalVariableExpression(var: !38, expr: !DIExpression())
!38 = distinct !DIGlobalVariable(scope: null, file: !3, line: 38, type: !39, isLocal: true, isDefinition: true)
!39 = !DICompositeType(tag: DW_TAG_array_type, baseType: !11, size: 48, elements: !40)
!40 = !{!41}
!41 = !DISubrange(count: 6)
!42 = !DIGlobalVariableExpression(var: !43, expr: !DIExpression())
!43 = distinct !DIGlobalVariable(scope: null, file: !3, line: 44, type: !44, isLocal: true, isDefinition: true)
!44 = !DICompositeType(tag: DW_TAG_array_type, baseType: !11, size: 128, elements: !45)
!45 = !{!46}
!46 = !DISubrange(count: 16)
!47 = !DIGlobalVariableExpression(var: !48, expr: !DIExpression())
!48 = distinct !DIGlobalVariable(scope: null, file: !3, line: 45, type: !49, isLocal: true, isDefinition: true)
!49 = !DICompositeType(tag: DW_TAG_array_type, baseType: !11, size: 168, elements: !50)
!50 = !{!51}
!51 = !DISubrange(count: 21)
!52 = !{i32 7, !"Dwarf Version", i32 5}
!53 = !{i32 2, !"Debug Info Version", i32 3}
!54 = !{i32 1, !"wchar_size", i32 4}
!55 = !{i32 8, !"PIC Level", i32 2}
!56 = !{i32 7, !"PIE Level", i32 2}
!57 = !{i32 7, !"uwtable", i32 2}
!58 = !{i32 7, !"frame-pointer", i32 2}
!59 = !{!"Ubuntu clang version 18.1.8 (++20240731025043+3b5b5c1ec4a3-1~exp1~20240731145144.92)"}
!60 = distinct !DISubprogram(name: "print_person", scope: !3, file: !3, line: 17, type: !61, scopeLine: 17, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !2, retainedNodes: !65)
!61 = !DISubroutineType(types: !62)
!62 = !{null, !63}
!63 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !64, size: 64)
!64 = !DIDerivedType(tag: DW_TAG_const_type, baseType: !6)
!65 = !{}
!66 = !DILocalVariable(name: "p", arg: 1, scope: !60, file: !3, line: 17, type: !63)
!67 = !DILocation(line: 0, scope: !60)
!68 = !DILocation(line: 18, column: 29, scope: !60)
!69 = !DILocation(line: 18, column: 26, scope: !60)
!70 = !DILocation(line: 18, column: 5, scope: !60)
!71 = !DILocation(line: 19, column: 28, scope: !60)
!72 = !DILocation(line: 19, column: 5, scope: !60)
!73 = !DILocation(line: 20, column: 1, scope: !60)
!74 = distinct !DISubprogram(name: "main", scope: !3, file: !3, line: 22, type: !75, scopeLine: 22, spFlags: DISPFlagDefinition, unit: !2, retainedNodes: !65)
!75 = !DISubroutineType(types: !76)
!76 = !{!15}
!77 = !DILocation(line: 24, column: 35, scope: !74)
!78 = !DILocalVariable(name: "personPtr", scope: !74, file: !3, line: 24, type: !5)
!79 = !DILocation(line: 0, scope: !74)
!80 = !DILocation(line: 25, column: 40, scope: !74)
!81 = !DILocalVariable(name: "test", scope: !74, file: !3, line: 25, type: !16)
!82 = !DILocation(line: 27, column: 19, scope: !83)
!83 = distinct !DILexicalBlock(scope: !74, file: !3, line: 27, column: 9)
!84 = !DILocation(line: 27, column: 9, scope: !74)
!85 = !DILocation(line: 28, column: 9, scope: !86)
!86 = distinct !DILexicalBlock(scope: !83, file: !3, line: 27, column: 28)
!87 = !DILocation(line: 29, column: 9, scope: !86)
!88 = !DILocation(line: 32, column: 14, scope: !89)
!89 = distinct !DILexicalBlock(scope: !74, file: !3, line: 32, column: 9)
!90 = !DILocation(line: 32, column: 9, scope: !74)
!91 = !DILocation(line: 33, column: 9, scope: !92)
!92 = distinct !DILexicalBlock(scope: !89, file: !3, line: 32, column: 23)
!93 = !DILocation(line: 34, column: 9, scope: !92)
!94 = !DILocation(line: 38, column: 23, scope: !74)
!95 = !DILocation(line: 38, column: 12, scope: !74)
!96 = !DILocation(line: 38, column: 5, scope: !74)
!97 = !DILocation(line: 39, column: 16, scope: !74)
!98 = !DILocation(line: 39, column: 20, scope: !74)
!99 = !DILocation(line: 40, column: 11, scope: !74)
!100 = !DILocation(line: 40, column: 17, scope: !74)
!101 = !DILocation(line: 43, column: 5, scope: !74)
!102 = !DILocation(line: 44, column: 38, scope: !74)
!103 = !DILocation(line: 44, column: 5, scope: !74)
!104 = !DILocation(line: 45, column: 37, scope: !74)
!105 = !DILocation(line: 45, column: 5, scope: !74)
!106 = !DILocation(line: 48, column: 5, scope: !74)
!107 = !DILocation(line: 49, column: 5, scope: !74)
!108 = !DILocation(line: 51, column: 5, scope: !74)
!109 = !DILocation(line: 52, column: 1, scope: !74)
